
from playwright.async_api import Page

async def rating(page:Page):
        ratings = 0
        ratings_locator = page.locator("span#acrCustomerReviewText").first
        if await ratings_locator.count() > 0:
            ratings_text = await ratings_locator.text_content()
            ratings = ratings_text.split(" ")[0].replace(",", "").strip() if ratings_text else 0
        else:
            ratings = 0
        
        return ratings