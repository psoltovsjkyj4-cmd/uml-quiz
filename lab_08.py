import re

def lint_diff(text: str, rules=None, max_changes: int = 400) -> list[dict]:
if rules is not None:
valid_rules = {"R001", "R002", "R003", "R004", "R005", "R006"}
for r in sorted(rules):
if r not in valid_rules:
raise ValueError(f"Невідоме правило: {r}")

lines = text.splitlines(keepends=False)
issues = []

current_file = ""
current_line_no = 0
total_changes = 0

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("+++ b/"):
        current_file = line[6:]
        current_line_no = 0
        i += 1
        continue
    elif line.startswith("@@"):
        match = re.search(r'\+(\d+)', line)
        if match:
            current_line_no = int(match.group(1)) - 1
        i += 1
        continue
        
    if line.startswith("+") and not line.startswith("+++"):
        total_changes += 1
        content = line[1:]
        current_line_no += 1
        
        if rules is None or "R001" in rules:
            if re.search(r'\b(TODO|FIXME)\b', content):
                issues.append({"path": current_file, "line": current_line_no, "code": "R001"})
                
        if rules is None or "R002" in rules:
            if re.search(r'\bprint\s*\(', content):
                issues.append({"path": current_file, "line": current_line_no, "code": "R002"})
                
        if rules is None or "R003" in rules:
            if content.endswith(" ") or content.endswith("\t"):
                issues.append({"path": current_file, "line": current_line_no, "code": "R003"})
    elif line.startswith("-") and not line.startswith("---"):
        total_changes += 1
    elif not line.startswith("\\"):
        if current_line_no > 0 or line.startswith(" "):
            current_line_no += 1
    i += 1
    
if total_changes > max_changes:
    issues.append({"path": "", "line": 0, "code": "R006"})
    
return issues
