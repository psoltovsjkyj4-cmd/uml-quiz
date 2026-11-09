def render_fragments(participants, body, numbered=False):
lines = ["@startuml"]
if numbered:
lines.append("autonumber")

for p_type, p_name in participants:
    lines.append(f"{p_type} {p_name}")
    
def process_body(elements, indent=0):
    pad = "    " * indent
    for el in elements:
        if isinstance(el, tuple):
            kind = el[0]
            if kind == "msg":
                _, sender, receiver, text = el
                lines.append(f"{pad}{sender} -> {receiver} : {text}")
            elif kind == "ret":
                _, sender, receiver, text = el
                lines.append(f"{pad}{sender} --> {receiver} : {text}")
            elif kind == "alt":
                branches = el[1:]
                for i, (cond, branch_elements) in enumerate(branches):
                    if i == 0:
                        lines.append(f"{pad}alt {cond}")
                    else:
                        lines.append(f"{pad}else {cond}")
                    process_body(branch_elements, indent + 1)
                lines.append(f"{pad}end")
            elif kind == "opt":
                _, cond, opt_elements = el
                lines.append(f"{pad}opt {cond}")
                process_body(opt_elements, indent + 1)
                lines.append(f"{pad}end")
            elif kind == "loop":
                _, cond, loop_elements = el
                lines.append(f"{pad}loop {cond}")
                process_body(loop_elements, indent + 1)
                lines.append(f"{pad}end")
                
process_body(body)
lines.append("@enduml")
return "\n".join(lines)
