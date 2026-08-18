# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto('https://flk.npc.gov.cn/index', timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找搜索按钮
    btns = page.evaluate('''() => Array.from(document.querySelectorAll('button, span, i, div')).map(el => ({
        tag: el.tagName,
        class: el.className,
        text: (el.innerText || '').trim()
    })).filter(x => x.text === '搜索' || x.class.includes('search'))''')
    print("Search buttons/icons:", btns)
    b.close()
