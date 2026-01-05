from playwright.async_api import Page


async def brand_name(page: Page):
    brand_name_element = await page.query_selector("#bylineInfo_feature_div")
    if not brand_name_element:
        return None

    text = (await brand_name_element.text_content() or "").strip()

    # Find and clean text after "Visit the"
    keyword = "Visit the"
    if keyword in text:
        text = text.split(keyword, 1)[1].strip()  # get part after "Visit the"
    text = text.replace("Store", "").strip()

    return text
