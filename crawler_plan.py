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
    print("Found JS files:", js_files)
    
    for js in js_files:
        if not js.startswith('http'):
            js_url = 'https://surff.kr' + (js if js.startswith('/') else '/' + js)
        else:
            js_url = js
        print(f"Fetching {js_url}...")
        try:
            req_js = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})
            js_content = urllib.request.urlopen(req_js, context=ctx).read().decode('utf-8', errors='ignore')
            
            # Look for API endpoints
            apis = re.findall(r'https?://[^"\'\s>]+api[^"\'\s>]*', js_content)
            apis += re.findall(r'/api/[^"\'\s>]*', js_content)
            
            # Also look for graphql or specific fare endpoints
            apis += re.findall(r'/[^"\'\s>]*fare[^"\'\s>]*', js_content)
            
            if apis:
                print(f"Found potential APIs:", list(set(apis))[:20])
        except Exception as e:
            print(f"Failed to fetch {js_url}: {e}")
except Exception as e:
    print(f"Error: {e}")
