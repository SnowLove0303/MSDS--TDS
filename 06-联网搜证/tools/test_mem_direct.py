# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto('https://www.mem.gov.cn/fw/flfgbz/fg/fl_6143/202107/t20210716_416558.shtml', timeout=30000)
    page.wait_for_timeout(2000)
    print("MEM Title:", page.title())
    body = page.evaluate('''() => {
        const el = document.querySelector('.article-content, #content, .content, .main_content, .view_content, body');
        return el ? el.innerText : '';
    }''')
    print("MEM Content len:", len(body))
    print("Sample:\n", body[:400])
    b.close()
