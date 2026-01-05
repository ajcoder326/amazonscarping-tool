import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Get the default executable path for Playwright's Chromium
        chromium_path = p.chromium.executable_path
        print("Playwright Chromium executable path:", chromium_path)

        # Just to verify the browser launches
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
