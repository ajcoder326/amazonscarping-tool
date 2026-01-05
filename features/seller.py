from playwright.async_api import Page

async def seller(page:Page):
        seller_locator = page.locator("#sellerProfileTriggerId").first
        seller = (await seller_locator.text_content()).strip() if await seller_locator.count() > 0 else None
        return seller