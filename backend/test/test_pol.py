import asyncio
from playwright.async_api import async_playwright

async def capture_pol_modal():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        try:
            print("Navigating...")
            await page.goto("https://surff.kr/fare", wait_until="networkidle")
            await page.wait_for_timeout(3000)
            
            print("Clicking POL button...")
            await page.click('button.e14tdgw76:has-text("KRPUS")')
            await page.wait_for_timeout(2000)
            
            print("Capturing snapshot...")
            html = await page.content()
            with open("snapshot_pol.html", "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_pol_modal())
