# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://hbba.sacinfo.org.cn/stdDetail/237e8c3bcf5d6c810d7b233a7e53fca8"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto("https://hbba.sacinfo.org.cn/stdList?key=WS%20444", timeout=30000)
    page.wait_for_timeout(2000)
    
    links = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('WS') || x[0].includes('中毒'))''')
    print("WS 444 links:", links)
    
    page.goto("https://hbba.sacinfo.org.cn/stdList?key=GBZ%2071", timeout=30000)
    page.wait_for_timeout(2000)
    links_gbz = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('GBZ') || x[0].includes('中毒'))''')
    print("GBZ 71 links:", links_gbz)
    b.close()
