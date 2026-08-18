# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto("https://cn.bing.com/search?q=%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7%E6%B3%95+site%3Agov.cn", timeout=20000)
    page.wait_for_timeout(2000)
    print("Bing Title:", page.title())
    results = page.evaluate('''() => {
        const items = document.querySelectorAll('li.b_algo');
        return Array.from(items).map(item => {
            const h2 = item.querySelector('h2');
            const a = h2 ? h2.querySelector('a') : item.querySelector('a');
            return {
                title: h2 ? h2.innerText.trim() : '',
                href: a ? a.href : ''
            };
        });
    }''')
    print("Found items:", len(results))
    for r in results[:5]:
        print("  ", r)
    b.close()
