
from playwright.async_api import Page
async def browser_node(page:Page):
        breadcrumb_locator = page.locator(
            "div#wayfinding-breadcrumbs_feature_div ul.a-unordered-list.a-horizontal.a-size-small a"
            )

        # Check if any breadcrumb links exist
        if await breadcrumb_locator.count() > 0:
            # Get text content of all <a> elements
            browse_node_list = await breadcrumb_locator.all_inner_texts()
            # Join them with ' > '
            browse_node = " > ".join(text.strip() for text in browse_node_list)
            return browse_node
        else:
            return None