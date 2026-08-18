# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto("https://www.so.com/s?q=易制爆危险化学品名录+2017年版+完整版", timeout=30000)
    page.wait_for_timeout(2000)
    
    links = page.evaluate('''() => Array.from(document.querySelectorAll('h3 a, .res-title a')).map(a => [(a.innerText || '').trim(), a.href]);''')
    print("360 易制爆 links:")
    for l in links[:6]:
        print("  ", l)
    b.close()
