# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.baidu.com/s?wd=中华人民共和国安全生产法%202021%20全文", timeout=30000)
    page.wait_for_timeout(2000)
    
    results = page.evaluate('''() => {
        const rows = document.querySelectorAll('.result, .c-container');
        return Array.from(rows).map(r => {
            const h3 = r.querySelector('h3');
            const a = r.querySelector('a');
            return {
                title: h3 ? h3.innerText.trim() : (a ? a.innerText.trim() : ''),
                href: a ? a.href : ''
            };
        }).filter(x => x.title && x.href);
    }''')
    print("Found Baidu results:", len(results))
    for r in results[:8]:
        print("  ", r)
    b.close()
