# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/gb/index', timeout=30000)
    page.wait_for_timeout(2000)
    links = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].length > 1)''')
    for l in links[:30]:
        print("  ", l)
    b.close()
