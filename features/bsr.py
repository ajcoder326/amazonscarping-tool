async def bsr(page):
    bsr1, bsr2 = "N/A", "N/A"
    table = page.locator("table#productDetails_detailBullets_sections1").first
    if await table.count() > 0:
        th_elements = await table.locator("th").all()
        best_sellers_th = None
        for th in th_elements:
            text = (await th.text_content() or "").strip()
            if text == "Best Sellers Rank":
                best_sellers_th = th
                break
        if best_sellers_th:
            best_sellers_td = await best_sellers_th.evaluate_handle("th => th.nextElementSibling")
            if best_sellers_td:
                span_texts = await best_sellers_td.eval_on_selector_all(
                    "span", "spans => spans.map(s => s.textContent.trim())"
                )
                ranks_str = " ".join(span_texts)
                ranks = ranks_str.split("#")[1:3]
                if span_texts:
                    ranks = ranks_str.split("#")[1:3]
                    if len(ranks) < 2:
                        ranks += ["Not Available"] * (2 - len(ranks))
                    bsr1, bsr2 = ranks[0], ranks[1]
                else:
                    bsr1, bsr2 = "N/A", "N/A"
    return f"{bsr1}, {bsr2}"