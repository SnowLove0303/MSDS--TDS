# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.sogou.com/web?query=GB+15258-2009+全文", timeout=20000)
    page.wait_for_timeout(2500)
    print("Sogou Title:", page.title())
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('h3 a, .vr-title a, .rb a')).map(a => [(a.innerText || '').trim(), a.href]);
    }''')
    print("Sogou links found:", len(links))
    for l in links[:10]:
        print("  ", l)
    b.close()
