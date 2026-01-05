
from playwright.async_api import Page
async def price(page:Page):
    price = 0
    price_loc = page.locator("span.a-price-whole")
    if await price_loc.count() > 0:
            price_text = await price_loc.first.text_content()
            if price_text:
                price = price_text.strip()
    return price