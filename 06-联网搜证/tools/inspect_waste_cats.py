# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找所有子分类
    links = page.evaluate('''() => Array.from(document.querySelectorAll('.tab_con a, .main_content a, .content_list a, ul li a')).map(a => [(a.innerText || '').trim(), a.href]).filter(x => x[0].includes('固体') || x[0].includes('危险') || x[0].includes('危废') || x[0].includes('化学品'));''')
    print("MEE Waste/Chemical standards categories:")
    for l in links:
        print("  ", l)
    b.close()
