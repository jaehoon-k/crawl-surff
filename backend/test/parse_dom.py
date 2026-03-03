from bs4 import BeautifulSoup

with open("snapshot.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
inputs = soup.find_all('input')
for inp in inputs:
    print(f"Input: {inp.get('placeholder', 'NO_PLACEHOLDER')} | ID: {inp.get('id', '')} | Class: {inp.get('class', '')}")

buttons = soup.find_all('button')
for btn in buttons:
    print(f"Button text: {btn.text.strip()} | Class: {btn.get('class', '')}")
