# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=download&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    print("Download page scripts:")
    scripts = page.evaluate('''() => Array.from(document.querySelectorAll('script')).map(s => s.innerText)''')
    for idx, s in enumerate(scripts):
        if 'verify' in s or 'viewGb' in s or 'download' in s:
            print(f"=== Script {idx+1} ===")
            print(s)
    b.close()
