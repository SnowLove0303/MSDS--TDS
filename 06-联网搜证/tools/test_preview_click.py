# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 监听新打开的页面或请求
    with context.expect_page() as new_page_info:
        page.click("button:has-text('在线预览')")
    preview_page = new_page_info.value
    preview_page.wait_for_load_state()
    preview_page.wait_for_timeout(3000)
    print("Preview Page URL:", preview_page.url)
    print("Preview Page Title:", preview_page.title())
    b.close()
