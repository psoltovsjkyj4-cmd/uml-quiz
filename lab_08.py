def lint_diff(text, rules=None, max_changes=400):
if rules is None:
rules = {"R001", "R002", "R003", "R004", "R005", "R006"}
else:
rules = set(rules)

known_rules = {"R001", "R002", "R003", "R004", "R005", "R006"}
for r in rules:
    if r not in known_rules:
        raise ValueError(f"Невідоме правило: {r}")

lines = text.splitlines(keepends=False)
issues = []

current_file = ""
current_line_num = 0
added_count = 0
deleted_count = 0

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("diff --git"):
        parts = line.split(" b/")
        if len(parts) > 1:
            current_file = parts[1]
        else:
            current_file = ""
    elif line.startswith("@@"):
        pos = line.find("+")
        if pos != -1:
            hunk_part = line[pos+1:].split(" ")[0]
            if "," in hunk_part:
                current_line_num = int(hunk_part.split(",")[0]) - 1
            else:
                current_line_num = int(hunk_part) - 1
    elif line.startswith("+") and not line.startswith("+++"):
        current_line_num += 1
        added_count += 1
        content = line[1:]
        
        # R001: TODO або FIXME як окреме слово
        if "R001" in rules:
            import re
            if re.search(r'\b(TODO|FIXME)\b', content):
                issues.append({"path": current_file, "line": current_line_num, "code": "R001"})
        
        # R002: виклик print()
        if "R002" in rules:
            if "print(" in content:
                issues.append({"path": current_file, "line": current_line_num, "code": "R002"})
                
        # R003: зайві пробіли чи табуляції в кінці рядка
        if "R003" in rules:
            if content.endswith(" ") or content.endswith("\t"):
                if content.strip() != "":
                    issues.append({"path": current_file, "line": current_line_num, "code": "R003"})
                    
    elif line.startswith("-") and not line.startswith("---"):
        deleted_count += 1
    elif line.startswith(" ") or line == "":
        if line.startswith(" "):
            current_line_num += 1

if "R006" in rules and (added_count + deleted_count) > max_changes:
    issues.append({"path": "", "line": 0, "code": "R006"})

return issues
