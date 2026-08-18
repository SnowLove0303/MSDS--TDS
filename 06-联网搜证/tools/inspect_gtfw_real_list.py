# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/gthw/gtfwwrkzbz/"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找列表中所有的链接
    items = page.evaluate('''() => {
        const as = Array.from(document.querySelectorAll('.main_content a, .content_list a, ul.list li a, .table_list a, a'));
        return as.map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('GB') || x[0].includes('标准') || x[0].includes('HJ'));
    }''')
    print("Found MEE Standard items in GTFW category:", len(items))
    for it in items[:25]:
        print("  ", it)
    b.close()
