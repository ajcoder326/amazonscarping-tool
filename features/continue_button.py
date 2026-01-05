   
from playwright.async_api import Page
import re
async def continue_button(page:Page):
        button = page.locator("button", has_text=re.compile(r'continue shopping', re.IGNORECASE))
        if await button.count() > 0 and await button.is_visible():
            try:
                await button.click()
            except Exception as e:
                status = 'Suppressed Continue Button'
                return status