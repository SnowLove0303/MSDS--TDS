# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto("https://www.baidu.com/s?wd=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7%E6%B3%95+site%3Agov.cn", timeout=20000)
    page.wait_for_timeout(2000)
    print("Title:", page.title())
    results = page.evaluate('''() => {
        const items = document.querySelectorAll('.result, .c-container');
        return Array.from(items).map(item => {
            const h3 = item.querySelector('h3');
            const a = h3 ? h3.querySelector('a') : item.querySelector('a');
            return {
                title: h3 ? h3.innerText.trim() : '',
                href: a ? a.href : ''
            };
        });
    }''')
    print("Found items:", len(results))
    for r in results[:5]:
        print("  ", r)
    b.close()
