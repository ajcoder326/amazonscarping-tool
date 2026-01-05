
from playwright.async_api import Page

async def check_status(page: Page, asin: str):

        status: str = 'Suppressed Default'
        current_url: str = page.url

        # Expected rush hour message prefix
        expected_message_start = "Oops! It's rush hour and traffic is piling up on that page."


        try:
        
            unexpected_page_text = "Looking for something?"
            locator = page.locator("table b", has_text=unexpected_page_text)

            # Wait up to 10 seconds for it to appear
            await locator.wait_for(state="attached",timeout=50_00)

            # Use .first to avoid strict mode violation
            text = await locator.first.text_content()

            # Compare the text safely
            if text and text.strip().startswith(unexpected_page_text):
                status = "Suppressed Detail Page Removed"
                print("🟡 Suppressed Detail Page Removed.")
                return status

        except Exception as e:
            pass
  

        # Check for rush hour message in a <center> element
        rush_hour_element = await page.query_selector("center")
        if rush_hour_element:
            text_content = await rush_hour_element.text_content()
            clean_text = ' '.join([line.strip() for line in text_content.splitlines() if line.strip()])
            if clean_text.startswith(expected_message_start):
                return 'Rush Hour'

        if 'dp' in current_url:
            # Check if suppression warning is present
            suppressed_element = await page.query_selector(".h1")
            if suppressed_element:
                status = 'Suppressed Warning Found'
            else:
                # Locate the ASIN  element
                asin_element = page.locator('div[data-card-metrics-id^="tell-amazon-desktop_DetailPage_"] div[data-asin]')
                try:
                    await asin_element.wait_for(state="visible", timeout=20000)
                    main_data_asin_val = await asin_element.get_attribute("data-asin")
                    if main_data_asin_val == asin:
                        status = 'Live'
                    else:
                        status = 'Suppressed Asin Changed'
                except Exception:
                    # html = await page.content()
                    # print(html)
                    # print()
                    # print()
                    # print()
                    status = 'Suppressed Detail Page Removed'

        return status

