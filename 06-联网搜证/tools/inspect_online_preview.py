# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=online&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(3000)
    print("Page Title:", page.title())
    print("Page URL:", page.url)
    iframe_src = page.evaluate('''() => {
        const f = document.querySelector('iframe');
        return f ? f.src : 'NO_IFRAME';
    }''')
    print("Iframe Src:", iframe_src)
    b.close()
