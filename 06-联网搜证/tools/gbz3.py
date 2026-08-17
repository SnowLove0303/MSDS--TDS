# -*- coding: utf-8 -*-
"""Playwright 访问卫健委官网: 首页建立cookie -> 搜 GBZ 2.1"""
import time
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page()
    pg.goto('https://www.nhc.gov.cn/', timeout=45000, wait_until='domcontentloaded')
    pg.wait_for_timeout(5000)
    print('首页:', pg.title()[:50], '|', pg.url[:70])
    # 找搜索框
    try:
        # 卫健委站内搜索URL: 使用 site 参数
        pg.goto('https://www.nhc.gov.cn/wjw/searchResultList.shtml?searchWord=GBZ+2.1', timeout=40000, wait_until='domcontentloaded')
        pg.wait_for_timeout(3000)
        body = pg.evaluate('() => document.body.innerText')
        print('搜索结果页 前600字:')
        print(body[:600])
    except Exception as e:
        print('搜索异常:', str(e)[:80])
    b.close()
