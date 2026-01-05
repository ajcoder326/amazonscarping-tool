

from playwright.async_api import Page

async def reviews(page:Page):
        reviews_locator = page.locator("span#acrPopover").first
        review = 0
        try:
            await reviews_locator.wait_for(state="visible", timeout=10000)
            reviews_title = await reviews_locator.get_attribute("title")
            reviews = reviews_title.split(" ")[0].strip() if reviews_title else "0"

        except:
            reviews = 0
        return reviews