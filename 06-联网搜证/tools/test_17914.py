# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "BD4BA33D46B2AD5DCA3F1EBA7E99BEE6" # GB 17914-2013

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    buttons = page.evaluate('''() => Array.from(document.querySelectorAll('button, a')).map(b => b.innerText.trim()).filter(Boolean)''')
    print("Buttons on GB 17914-2013:", buttons)
    b.close()
