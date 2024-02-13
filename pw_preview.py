import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # browser = await p.chromium.launch(headless=False)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(java_script_enabled=True)
        await page.set_viewport_size({'width': 1920, 'height':820})
        await page.goto('file:/home/user/bot/lcbot/test2.html')
        await page.wait_for_timeout(500)
        await page.screenshot(path='/home/user/bot/lcbot/source/screen.png')
        await page.close()
        await browser.close()

asyncio.run(main())