import urllib.request
import urllib.parse
import json

def test_api():
    url = "http://localhost:8000/api/fares"
    params = {
        "cntr_type": "40 Dry",
        "pol": "KRPUS",
        "pod": "USBOS",
        "period": "6개월"
    }
    qs = urllib.parse.urlencode(params)
    full_url = f"{url}?{qs}"
    print(f"Calling {full_url}")
    try:
        response = urllib.request.urlopen(full_url)
        print("Status:", response.status)
        data = json.loads(response.read().decode('utf-8'))
        if data.get("data") and data["data"].get("resultObject"):
            graph = data["data"]["resultObject"].get("graphData", [])
            print(f"Got {len(graph)} data points.")
            if len(graph) > 0:
                print("First:", graph[0]["weekStartDate"])
                print("Last:", graph[-1]["weekEndDate"])
        else:
            print("No data")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
