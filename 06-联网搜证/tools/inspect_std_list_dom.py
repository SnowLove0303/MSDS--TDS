# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/gb/std_list', timeout=30000)
    page.wait_for_timeout(3000)
    print("URL:", page.url)
    print("Title:", page.title())
    inputs = page.evaluate('''() => Array.from(document.querySelectorAll('input, button, select')).map(el => ({
        tag: el.tagName,
        id: el.id,
        name: el.name,
        class: el.className,
        type: el.type,
        placeholder: el.placeholder || '',
        value: el.value || ''
    }))''')
    for inp in inputs:
        print("  ", inp)
    b.close()
