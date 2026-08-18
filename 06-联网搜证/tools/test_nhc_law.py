# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.nhc.gov.cn/fzs/s3576/201812/e841249f3e494e82845e69e46a782b13.shtml", timeout=30000)
    page.wait_for_timeout(2000)
    print("NHC Title:", page.title())
    content = page.evaluate('''() => {
        const el = document.querySelector('#con, .con, #view_content, .article-content, #content, body');
        return el ? el.innerText : '';
    }''')
    print("Content len:", len(content))
    print("Sample:\n", content[:300])
    b.close()
