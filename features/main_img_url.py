

from playwright.async_api import Page

async def main_img_url(page:Page):
        main_img_url = ''
        try:
            ul_locator = page.locator(
                "ul.a-unordered-list.a-nostyle.a-button-list.a-vertical.a-spacing-top-micro.gridAltImageViewLayoutIn1x7"
            ).first
            if await ul_locator.count() == 0:
                ul_locator = page.locator(
                    "ul.a-unordered-list.a-nostyle.a-button-list.a-vertical.a-spacing-top-extra-large.regularAltImageViewLayout"
                ).first

            if await ul_locator.count() > 0:
                img_locators = ul_locator.locator("img")
                count = await img_locators.count()
                for i in range(count):
                    src = await img_locators.nth(i).get_attribute("src")
                    if src and src.endswith(".jpg"):
                        main_img_url = src.replace("SS100", "SS500")
                        break
        except Exception as e:
            return ''
        return main_img_url
