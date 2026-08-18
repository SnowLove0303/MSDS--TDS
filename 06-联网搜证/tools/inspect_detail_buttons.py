# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    buttons = page.evaluate('''() => Array.from(document.querySelectorAll('button, a, input[type="button"]')).map(b => ({
        tag: b.tagName,
        text: (b.innerText || '').trim(),
        onclick: b.getAttribute('onclick') || '',
        href: b.href || ''
    })).filter(x => x.text || x.onclick)''')
    for b_item in buttons:
        print("  ", b_item)
    b.close()
