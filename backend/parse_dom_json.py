import json
from bs4 import BeautifulSoup

with open("snapshot_pol.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
data = {"inputs": [], "buttons": []}

inputs = soup.find_all('input')
for inp in inputs:
    data["inputs"].append({
        "placeholder": inp.get("placeholder", ""),
        "id": inp.get("id", ""),
        "class": " ".join(inp.get("class", []))
    })

buttons = soup.find_all('button')
for btn in buttons:
    data["buttons"].append({
        "text": btn.text.strip(),
        "class": " ".join(btn.get("class", []))
    })

with open("dom_info.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
