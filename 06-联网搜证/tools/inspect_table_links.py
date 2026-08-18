# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import re

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/gb/std_list', timeout=30000)
    page.wait_for_timeout(2000)
    page.fill("input[name='search1']", "15258-2009")
    page.click("button#search1")
    page.wait_for_timeout(2500)
    
    # 获取所有的 a onclick 或者 href
    all_links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('table.table a, .table a, table tbody tr a')).map(a => ({
            text: a.innerText.trim(),
            href: a.href,
            onclick: a.getAttribute('onclick') || ''
        }));
    }''')
    print("Found links:", len(all_links))
    for l in all_links[:10]:
        print("  ", l)
    b.close()
