# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto("https://hbba.sacinfo.org.cn/stdList?key=JT/T%20617", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找所有 a 链接
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            text: (a.innerText || '').trim(),
            href: a.href
        })).filter(x => x.text.includes('JT/T') || x.text.includes('危险货物'));
    }''')
    print("JT links:", links)
    
    if links:
        page.goto(links[0]["href"], timeout=30000)
        page.wait_for_timeout(2000)
        print("Detail Page Title:", page.title())
        detail_text = page.evaluate('() => document.body.innerText')
        print("Detail Text Sample:\n", detail_text[:500])
    b.close()
