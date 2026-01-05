from playwright.async_api import Page
import re

async def mrp(page: Page) -> float | None:
    """
    Extracts the product's MRP (Maximum Retail Price) as a float value
    from the #corePriceDisplay_desktop_feature_div section.
    """
    # Directly target the element that holds the clean text
    element = await page.query_selector(
        "#corePriceDisplay_desktop_feature_div .basisPrice .a-offscreen"
    )
    if not element:
        return None

    text = (await element.text_content() or "").strip()
    # Example: "₹999"
    match = re.search(r"₹\s*([\d,]+)", text)
    if not match:
        return None

    try:
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None
