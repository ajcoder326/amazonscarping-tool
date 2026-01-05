import os
import csv
import aiofiles
from datetime import datetime
from typing import Dict

async def csv_audit_general(data: Dict[str, str], filepath: str) -> None:
    """Append data to CSV safely, handling commas, quotes, and newlines in values."""
    
    # Ensure folder exists
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    headers = [
        "asin",
        "proxy_ip",
        "status",
        "brand_name",
        "reviews",
        "ratings",
        "variations",
        "seller",
        "main_img_url",
        "price",
        "mrp",
        "deal",
        "browse_node",
        "availability",
        "quantity_showing",
        "bsr",
        "title",
        "timestamp",
    ]

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file exists and is not empty
    file_exists = os.path.isfile(filepath) and os.stat(filepath).st_size != 0

    # Use aiofiles + csv properly
    async with aiofiles.open(filepath, mode="a", newline="", encoding="utf-8") as f:
        # csv.DictWriter needs a *normal* file object, so wrap with a sync buffer
        import io
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=headers, quoting=csv.QUOTE_MINIMAL)

        if not file_exists:
            writer.writeheader()
        
        writer.writerow({h: data.get(h, "") for h in headers})

        # Write buffer content to aiofiles file
        await f.write(buffer.getvalue())
        await f.flush()
