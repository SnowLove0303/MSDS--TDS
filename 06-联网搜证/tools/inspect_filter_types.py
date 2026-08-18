# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/std/std_list', timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找所有类型选择的 checkbox / li
    types = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('.nav-pills a, input[type="checkbox"]')).map(el => ({
            tag: el.tagName,
            id: el.id,
            text: el.innerText ? el.innerText.trim() : '',
            value: el.value || '',
            className: el.className
        }));
    }''')
    for t in types[:30]:
        print("  ", t)
    b.close()
