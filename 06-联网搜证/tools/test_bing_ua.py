# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto("https://www.bing.com/search?q=中华人民共和国安全生产法+gov.cn", timeout=20000)
    page.wait_for_timeout(2500)
    print("Page Title:", page.title())
    print("Page URL:", page.url)
    anchors = page.evaluate('''() => Array.from(document.querySelectorAll('a')).map(a => [a.innerText.trim(), a.href]).filter(x => x[0].length > 3)''')
    for a in anchors[:15]:
        print("  ", a)
    b.close()
