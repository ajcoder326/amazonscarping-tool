
from playwright.async_api import Page
async def title(page:Page):
        title_locator = page.locator("span#productTitle").first
        try:
            await title_locator.wait_for(state="visible", timeout=5000)  # timeout in milliseconds
            title = await title_locator.text_content()
            if title:
                return title.strip()
        except Exception as e:         
            return ''