# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=online&hcno={hcno}&request_locale=zh", timeout=30000)
    page.wait_for_timeout(2000)
    print("Page HTML sample:")
    print(page.content()[:2000])
    b.close()
