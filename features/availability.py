from playwright.async_api import Page

async def availability(page:Page):
        availability = None
        availability_locator = page.locator("div#availability")
        if await availability_locator.count() > 0:
            availability_text = await availability_locator.first.inner_text()
            availability = availability_text.strip().split()[0] if availability_text else None
        return availability