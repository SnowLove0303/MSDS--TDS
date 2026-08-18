# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "67992CA972A4CF9222095CA06064724A" # GB/T 16483-2008

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=download&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    print("GB/T 16483 showGb page content length:", len(page.content()))
    inputs = page.evaluate('''() => Array.from(document.querySelectorAll('input, img')).map(el => el.id || el.src || el.name)''')
    print("Inputs on 16483:", inputs)
    b.close()
