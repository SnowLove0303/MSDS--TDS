# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "BD4BA33D46B2AD5DCA3F1EBA7E99BEE6" # GB 17914-2013 (有下载按钮)

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=download&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    
    html = page.content()
    print("showGb type=download HTML len:", len(html))
    inputs = page.evaluate('''() => Array.from(document.querySelectorAll('input, img, button')).map(el => ({
        tag: el.tagName,
        id: el.id,
        name: el.name,
        src: el.src || '',
        class: el.className
    }))''')
    for inp in inputs:
        print("  ", inp)
    b.close()
