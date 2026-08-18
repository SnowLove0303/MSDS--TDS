# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gthw/gtfwwrkzbz/index.shtml"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    links = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('18484') || x[0].includes('焚烧'));''')
    print("Found 18484 links:", links)
    
    if links:
        page.goto(links[0][1], timeout=30000)
        page.wait_for_timeout(2000)
        pdf_links = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[1].endsWith('.pdf'))''')
        print("18484 PDF Link:", pdf_links)
        if pdf_links:
            out_dest = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库与推断引擎\法规匹配库\标准原文归档\环保与危废\GB 18484-2020 危险废物焚烧污染控制标准.pdf")
            r = requests.get(pdf_links[0][1], headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
            out_dest.write_bytes(r.content)
            print(f"✅ 成功下载: {out_dest.name} ({len(r.content)} 字节)")
    b.close()
