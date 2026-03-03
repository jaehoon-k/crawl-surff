import urllib.request
import json

def test_raw_api():
    url = "https://cms.surff.kr/api/freight/port?cntType=40&polCode=KRPUS&podCode=USBOS&startDate=2026-01-27&endDate=2026-06-27"
    print(f"Calling RAW URL: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        graph = data.get("resultObject", {}).get("graphData", [])
        print(f"Got {len(graph)} data points.")
        if len(graph) > 0:
            print("First:", graph[0]["weekStartDate"])
            print("Last:", graph[-1]["weekEndDate"])
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_raw_api()
