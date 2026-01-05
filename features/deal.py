from playwright.async_api import Page

async def deal(page:Page):
    # Added .dealBadge and #dealBadgeSupportingText from inspection
    deal_locator = page.locator("span.dealBadgeTextColor, #dealBadgeSupportingText, .dealBadge, div.badge-label, #dealBadge, .amz-deal-text").first
    deal = "NA"
    if await deal_locator.count() > 0:
        deal_text = await deal_locator.text_content()
        if deal_text:
            deal_text_lower = deal_text.lower()
            if "limited time deal" in deal_text_lower:
                deal = "Limited time deal"
            elif "deal" in deal_text_lower:
                 deal = deal_text.strip()
    return deal