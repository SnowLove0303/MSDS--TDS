# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/fl/202004/t20200430_777580.shtml"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    print("MEE Gufei Title:", page.title())
    body = page.evaluate('() => document.querySelector(".content_body, #main_content, .article-content, body").innerText')
    print("Len:", len(body))
    print("Sample:", body[:300])
    b.close()
