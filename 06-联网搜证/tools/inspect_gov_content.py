# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.gov.cn/flfg/2014-09/01/content_2743841.htm"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    html = page.evaluate('''() => {
        const body = document.querySelector('#UCAP-CONTENT, td.p1, .pages_content');
        return body ? body.innerText : document.body.innerText;
    }''')
    print("Gov.cn content length:", len(html))
    print("Gov.cn content sample:\n", html[:500])
    b.close()
