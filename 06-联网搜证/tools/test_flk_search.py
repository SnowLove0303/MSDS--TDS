# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto('https://flk.npc.gov.cn/index', timeout=30000)
    page.wait_for_timeout(2000)
    
    # 输入安全生产法
    page.fill('input[placeholder="请输入"]', '安全生产法')
    page.keyboard.press('Enter')
    page.wait_for_timeout(3000)
    print("After search URL:", page.url)
    print("After search Title:", page.title())
    
    # 查看结果列表
    items = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('.result-item, .law-item, .list-item, .table-row, a')).map(el => ({
            text: (el.innerText || '').trim(),
            href: el.href || ''
        })).filter(x => x.text.includes('安全生产法'));
    }''')
    print("Found items:", len(items))
    for it in items[:10]:
        print("  ", it)
    b.close()
