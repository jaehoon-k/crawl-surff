from playwright.async_api import async_playwright
import asyncio

async def capture_snapshot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        try:
            print("Navigating...")
            await page.goto("https://surff.kr/fare", wait_until="networkidle")
            print("Waited for network idle. Now waiting 5 seconds for JS to render...")
            await asyncio.sleep(5)
            html = await page.content()
            with open("snapshot.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Snapshot saved to snapshot.html")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_snapshot())
