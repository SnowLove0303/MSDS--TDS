# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()
    page.goto("https://www.baidu.com/s?wd=中华人民共和国安全生产法%202021%20全文", timeout=30000)
    page.wait_for_timeout(2000)
    print("Direct Baidu Title:", page.title())
    b.close()
