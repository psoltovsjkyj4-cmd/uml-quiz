def screen_flow(html, stories):
import html.parser
import re
class ScreenParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.screens = {}
        self.current_screen = None
        self.screen_order = []
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if "data-screen" in attr_dict:
            sid = attr_dict["data-screen"].strip()
            if not sid:
                raise ValueError("Екран без id")
            if sid in self.screens:
                raise ValueError(f"Повторний екран: {sid}")
            self.current_screen = sid
            self.screen_order.append(sid)
            
            stories_attr = attr_dict.get("data-story", "")
            st_list = [s.strip() for s in re.split(r'[\s,]+', stories_attr) if s.strip()]
            
            self.screens[sid] = {
                "stories": st_list,
                "goto": set()
            }
        
        if self.current_screen:
            if tag == "a" and "href" in attr_dict:
                href = attr_dict["href"]
                if href.startswith("#") and len(href) > 1:
                    self.screens[self.current_screen]["goto"].add(href[1:])
            if "data-goto" in attr_dict:
                target = attr_dict["data-goto"].strip()
                if target:
                    self.screens[self.current_screen]["goto"].add(target)

parser = ScreenParser()
if not html or not html.strip():
    raise ValueError("Немає екранiв")
    
parser.feed(html)

if not parser.screen_order:
    raise ValueError("Немає екранiв")

screens_list = parser.screen_order
first_screen = screens_list[0] if screens_list else None

reachable = set()
if first_screen:
    queue = [first_screen]
    reachable.add(first_screen)
    while queue:
        curr = queue.pop(0)
        for nxt in parser.screens.get(curr, {}).get("goto", set()):
            if nxt in parser.screens and nxt not in reachable:
                reachable.add(nxt)
                queue.append(nxt)

unreachable = [s for s in screens_list if s not in reachable]
dead_ends = [s for s in screens_list if not parser.screens.get(s, {}).get("goto") and s in reachable]

coverage = {st: [] for st in stories}
uncovered = []

for sid in screens_list:
    for st in parser.screens[sid]["stories"]:
        if st in coverage:
            if sid not in coverage[st]:
                coverage[st].append(sid)

for st in stories:
    if not coverage[st]:
        uncovered.append(st)

unknown = {}
for sid in screens_list:
    for st in parser.screens[sid]["stories"]:
        if st not in stories:
            if st not in unknown:
                unknown[st] = []
            if sid not in unknown[st]:
                unknown[st].append(sid)

return {
    "screens": screens_list,
    "reachable": [s for s in screens_list if s in reachable],
    "unreachable": unreachable,
    "dead_ends": dead_ends,
    "broken": [],
    "coverage": coverage,
    "uncovered": uncovered,
    "unknown": unknown
}
