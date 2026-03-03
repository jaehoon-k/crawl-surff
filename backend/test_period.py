from playwright.async_api import async_playwright
import asyncio
import json

async def test_period_buttons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        target_api_url = "/api/freight/port"
        
        async def handle_response(response):
            if target_api_url in response.url:
                if response.status == 200 and response.request.method != "OPTIONS":
                    print(f"Intercepted API Call: {response.url}")

        page.on("response", handle_response)
        
        try:
            print("Navigating...")
            await page.goto("https://surff.kr/fare", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            
            print("Filling form...")
            await page.locator("xpath=(//button[@id='select-trigger'])[1]").click()
            await page.wait_for_selector('li:has-text("40\'Dry")', timeout=5000)
            await page.locator('li:has-text("40\'Dry")').first.click()
            
            await page.locator("xpath=(//button[@id='select-trigger'])[2]").click()
            await page.wait_for_selector('li:has-text("KRPUS")', timeout=5000)
            await page.locator('li:has-text("KRPUS")').first.click()
            
            await page.fill("input[placeholder='도착지 항구를 입력해 주세요.']", "USBOS")
            await page.wait_for_selector("xpath=//span[contains(text(), 'USBOS')]/..", timeout=5000)
            await page.locator("xpath=//span[contains(text(), 'USBOS')]/..").first.click()
            
            print("Clicking search...")
            await page.locator("button.fare_main_search").click()
            await page.wait_for_timeout(5000)
            
            periods = ["1개월", "3개월", "6개월", "1년", "전체"]
            for period in periods:
                print(f"Clicking period: {period}")
                await page.locator(f"xpath=//button[text()='{period}']").click()
                await page.wait_for_timeout(3000)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_period_buttons())
