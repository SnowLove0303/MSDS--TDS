# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto('https://www.mem.gov.cn/fw/flfgbz/fg/fl_6143/', timeout=30000)
    page.wait_for_timeout(2000)
    print("MEM FL List Title:", page.title())
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].length > 3);
    }''')
    for l in links:
        print("  ", l)
    b.close()
