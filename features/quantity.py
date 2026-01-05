from playwright.async_api import Page

async def quantity(page: Page):
    """
    Check for Quantity and return the value showing (e.g. "1").
    Returns "N/A" if not found.
    """
    try:
        # 1. Try Amazon's custom dropdown prompt (visible text like "1")
        # Added #selectQuantity (stable container) as priority
        prompt = page.locator("#selectQuantity .a-dropdown-prompt, #a-autoid-0-announce .a-dropdown-prompt, .a-dropdown-prompt").first
        if await prompt.count() > 0 and await prompt.is_visible():
            text = await prompt.text_content()
            if text:
                clean_text = text.strip()
                # Return if it looks like a number
                if clean_text.isdigit():
                    return clean_text

        # 2. Try native select or input
        qty_input = page.locator("#quantity, select[name='quantity'], #selectQuantity").first
        if await qty_input.count() > 0:
            # Try getting value
            val = await qty_input.input_value()
            if val and val.strip():
                return val.strip()
            
            # If element exists but value is empty/null, it typically defaults to 1
            return "1"

    except Exception:
        pass
    
    return "N/A"
