from .rating import rating
from  playwright.async_api import Page

from .mrp               import mrp
from .deal              import deal
from .title             import title
from .price             import price
from .seller            import seller
from .rating            import rating
from .review            import reviews
from .status            import check_status
from .variation         import variation
from .brand_name        import brand_name
from .browse_node       import browser_node
from .availability      import availability
from .main_img_url      import main_img_url
from .continue_button   import continue_button
from .bsr               import bsr
from .quantity          import quantity

from utils.save_file import csv_audit_general


async def entry(page:Page, asin:str, filename:str, proxy_ip:str = "N/A"):

    result = {                    
            "asin"          : asin,
            "proxy_ip"      : proxy_ip,
            "bsr"           : f"",
            "mrp"           : "mrp",
            "deal"          : "N/A",
            "title"         : "N/A",
            "price"         : 0, 
            "seller"        : "N/A",
            "status"        : "Suppressed",
            "reviews"       : 0,
            "ratings"       : 0,
            "variations"    : "N/A",
            "brand_name"    : "N/A",
            "browse_node"   : "N/A",
            "availability"  : "N/A",
            "quantity_showing": "N/A",
            "main_img_url"  : "N/A",
            }

    await continue_button(page)
    status = await check_status(page, asin)
    if status in [ 'Suppressed Warning Found', 'Rush Hour', 'Suppressed Default', "Suppressed Detail Page Removed"]:
        result['status'] = status
        await csv_audit_general(result, filename)
        return

    result['bsr']          = await bsr(page)
    result['mrp']          = await mrp(page)
    result['deal']         = await deal(page)
    result['title']        = await title(page)
    result['price']        = await price(page)
    result['seller']       = await seller(page)
    result['status']       = await check_status(page, asin)
    result['reviews']      = await reviews(page)
    result['ratings']      = await rating(page)
    result['variations']   = await variation(page)
    result['brand_name']   = await brand_name(page)
    result['browse_node']  = await browser_node(page)
    result['main_img_url'] = await main_img_url(page)
    result['availability'] = await availability(page)
    result['quantity_showing'] = await quantity(page)

    await csv_audit_general(result, filename)
    return