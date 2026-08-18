# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.baidu.com", timeout=20000)
    page.wait_for_timeout(1000)
    print("Page title:", page.title())
    
    # 模拟真实输入并搜索
    page.fill('#kw', '中华人民共和国职业病防治法 全文 2018')
    page.click('#su')
    page.wait_for_timeout(3000)
    
    links = page.evaluate('''() => {
        const as = Array.from(document.querySelectorAll('h3 a, .c-title a'));
        return as.map(a => [(a.innerText || '').trim(), a.href]);
    }''')
    print("Baidu search results:", len(links))
    for l in links[:10]:
        print("  ", l)
    b.close()
