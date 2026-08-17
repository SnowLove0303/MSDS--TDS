# -*- coding: utf-8 -*-
"""卫生标准网: 选卫生健康委员会 -> 搜 GBZ 2.1"""
import time
from playwright.sync_api import sync_playwright
CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page()
    pg.goto('https://hbba.sacinfo.org.cn/', timeout=45000, wait_until='networkidle')
    pg.wait_for_timeout(2000)
    # 点击 卫生健康委员会
    try:
        pg.click('text=卫生健康委员会')
        pg.wait_for_timeout(3000)
        print('点击后URL:', pg.url)
        # 在查询框输入
        inputs = pg.query_selector_all('input')
        for i, inp in enumerate(inputs):
            ph = inp.get_attribute('placeholder') or ''
            print(f'  input[{i}] placeholder={ph}')
        # 尝试在第一个输入框输入 GBZ 2.1
        if inputs:
            inputs[0].fill('GBZ 2.1')
            pg.keyboard.press('Enter')
            pg.wait_for_timeout(3000)
        body = pg.evaluate('() => document.body.innerText')
        print('正文前1200字:')
        print(body[:1200])
    except Exception as e:
        print('交互异常:', str(e)[:100])
        body = pg.evaluate('() => document.body.innerText')
        print('页面正文:', body[:500])
    b.close()
