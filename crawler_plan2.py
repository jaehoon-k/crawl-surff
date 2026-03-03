import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://surff.kr/fare', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    js_files = re.findall(r'src="(.*?\.js)"', html)
    
    with open('apis_found.txt', 'w', encoding='utf-8') as f:
        f.write(f"Found JS files: {js_files}\n")
        
        for js in js_files:
            if not js.startswith('http'):
                js_url = 'https://surff.kr' + (js if js.startswith('/') else '/' + js)
            else:
                js_url = js
            f.write(f"Fetching {js_url}...\n")
            try:
                req_js = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})
                js_content = urllib.request.urlopen(req_js, context=ctx).read().decode('utf-8', errors='ignore')
                
                # Look for exact API endpoints or relevant terms
                apis = re.findall(r'https?://[^"\'\s>]+api[^"\'\s>]*', js_content)
                apis += re.findall(r'/api/[^"\'\s>]*', js_content)
                apis += re.findall(r'/[^"\'\s>]*fare[^"\'\s>]*', js_content)
                apis += re.findall(r'/[^"\'\s>]*trend[^"\'\s>]*', js_content)
                
                if apis:
                    f.write(f"Found potential APIs in {js_url}:\n")
                    for api in list(set(apis)):
                        f.write(f"  - {api}\n")
            except Exception as e:
                f.write(f"Failed to fetch {js_url}: {e}\n")
except Exception as e:
    with open('apis_found.txt', 'w', encoding='utf-8') as f:
        f.write(f"Error: {e}\n")
