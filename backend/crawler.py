from playwright.async_api import async_playwright
import asyncio
import json

async def crawl_fare_data(cntr_type: str, pol: str, pod: str, period: str = "6개월"):
    """
    Crawls fare trend data from surff.kr/fare
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        target_api_url = "/api/freight/port"
        fare_data = None
        
        async def handle_response(response):
            nonlocal fare_data
            if target_api_url in response.url:
                if response.status == 200 and response.request.method != "OPTIONS":
                    try:
                        data = await response.json()
                        if data:
                            fare_data = data
                    except Exception as e:
                        print(f"Error parsing JSON: {e}")

        page.on("response", handle_response)
        
        try:
            print(f"Navigating to surff.kr/fare...")
            await page.goto("https://surff.kr/fare", wait_until="networkidle")
            
            await page.wait_for_timeout(3000)
            
            print(f"Selecting Container: {cntr_type}")
            await page.locator("xpath=(//button[@id='select-trigger'])[1]").click()
            if cntr_type == "40 Dry":
                cntr_match = "40'Dry"
            elif cntr_type == "20 Dry":
                cntr_match = "20'Dry"
            else:
                cntr_match = cntr_type
            await page.wait_for_selector(f'li:has-text("{cntr_match}")', timeout=5000)
            await page.locator(f'li:has-text("{cntr_match}")').first.click()
            
            print(f"Selecting POL: {pol}")
            await page.locator("xpath=(//button[@id='select-trigger'])[2]").click()
            pol_code = pol.split("(")[0]
            await page.wait_for_selector(f'li:has-text("{pol_code}")', timeout=5000)
            await page.locator(f'li:has-text("{pol_code}")').first.click()
            
            print(f"Selecting POD: {pod}")
            pod_code = pod.split("(")[0]
            await page.fill("input[placeholder='도착지 항구를 입력해 주세요.']", pod_code)
            await page.wait_for_selector(f"xpath=//span[contains(text(), '{pod_code}')]/..", timeout=5000)
            await page.locator(f"xpath=//span[contains(text(), '{pod_code}')]/..").first.click()
            
            print("Clicking search and waiting for data...")
            await page.locator("button.fare_main_search").click()
            
            for _ in range(15): # wait up to 15 seconds
                if fare_data is not None:
                    break
                await asyncio.sleep(1)

            # Handle period selection
            if period != "6개월" and period in ["1개월", "3개월", "1년", "전체"]:
                print(f"Selecting Period: {period}")
                await page.wait_for_selector(f"xpath=//button[text()='{period}']", timeout=10000)
                
                initial_data = fare_data
                fare_data = None
                
                await page.locator(f"xpath=//button[text()='{period}']").click()
                
                for _ in range(5):
                    if fare_data is not None:
                        break
                    await asyncio.sleep(1)
                    
                if fare_data is None:
                    print("Did not receive new API response; returning previous data.")
                    fare_data = initial_data

        except Exception as e:
            print(f"Crawler error: {e}")
            raise e
        finally:
            await browser.close()
            
        # Local filtering safeguard to ensure exact requested period sizes are returned, 
        # protecting against servers emitting raw unpaginated blocks or limited test data environments.
        if period != "전체" and fare_data and "resultObject" in fare_data and "graphData" in fare_data["resultObject"]:
            graph = fare_data["resultObject"]["graphData"]
            graph.sort(key=lambda x: x.get("weekStartDate", ""), reverse=True)
            if period == "1개월":
                graph = graph[:4]
            elif period == "3개월":
                graph = graph[:13]
            elif period == "6개월":
                graph = graph[:26]
            elif period == "1년":
                graph = graph[:52]
            graph.sort(key=lambda x: x.get("weekStartDate", ""))
            fare_data["resultObject"]["graphData"] = graph

        return {"status": "success", "data": fare_data}

# For testing
if __name__ == "__main__":
    result = asyncio.run(crawl_fare_data("40 Dry", "KRPUS(BUSAN)", "USBOS", "1개월"))
    if result.get("data"):
        print("Data successfully captured!")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500] + "...\n(truncated)")
    else:
        print("Failed to capture data.")
