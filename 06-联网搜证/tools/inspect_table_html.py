# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/gb/std_list', timeout=30000)
    page.wait_for_timeout(2000)
    page.fill("input[name='search1']", "15258-2009")
    page.click("button#search1")
    page.wait_for_timeout(2500)
    html = page.evaluate('() => document.querySelector("table tbody").innerHTML')
    print("Table HTML:")
    print(html[:1500])
    b.close()
