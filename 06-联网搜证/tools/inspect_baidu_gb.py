# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.baidu.com/s?wd=GB%2015258-2009%20全文", timeout=20000)
    page.wait_for_timeout(2000)
    
    html = page.evaluate('() => document.body.innerHTML')
    print("HTML length:", len(html))
    
    # 查找所有的 a
    as_list = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].length > 3);
    }''')
    print("Links found:", len(as_list))
    for l in as_list[:15]:
        print("  ", l)
    b.close()
