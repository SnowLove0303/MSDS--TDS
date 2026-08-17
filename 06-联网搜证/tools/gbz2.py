# -*- coding: utf-8 -*-
"""用 Playwright 访问卫生健康标准网/卫健委找 GBZ 2.1-2019 全文."""
import time
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

candidates = [
    ('卫生健康标准网', 'https://wsbzw.nhc.gov.cn/'),
    ('卫健委官网', 'https://www.nhc.gov.cn/'),
]
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page()
    for name, url in candidates:
        try:
            pg.goto(url, timeout=40000, wait_until='domcontentloaded')
            pg.wait_for_timeout(2500)
            print(f'{name}: {pg.title()} | {pg.url}')
            print('  片段:', pg.evaluate('() => document.body.innerText.slice(0,300).replace(/\n/g," ")'))
            pg.screenshot(path=f'probe_{name}.png')
        except Exception as e:
            print(f'{name}: 异常 {str(e)[:80]}')
        print()
    b.close()
