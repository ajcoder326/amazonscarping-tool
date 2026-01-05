
from playwright.async_api import Page

async def variation(page:Page):
     variations_locator = page.locator(
            "#twister-plus-inline-twister, "
            "#variation_color_name, "
            "#variation_size_name, "
            "#inline-twister-row-pattern_name, "
            "#variation_style_name"
        )
     variations = "Available" if await variations_locator.count() > 0 else "NA"  
     return variations