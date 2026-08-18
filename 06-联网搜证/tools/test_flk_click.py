# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto('https://flk.npc.gov.cn/index', timeout=30000)
    page.wait_for_timeout(2000)
    
    # 填充输入框并点击搜索图标
    page.fill('.search-input input', '安全生产法')
    # 点击 el-input 后缀或者回车
    page.click('.el-input__suffix, .search-type')
    page.keyboard.press('Enter')
    page.wait_for_timeout(3000)
    
    print("URL after action:", page.url)
    b.close()
