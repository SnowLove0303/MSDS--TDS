# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找所有 script 标签内容中含有的 url
    scripts = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('script')).map(s => s.innerText).filter(t => t.includes('preview') || t.includes('download') || t.includes('showGb') || t.includes('viewGb') || t.includes('hcno'));
    }''')
    for idx, s in enumerate(scripts):
        print(f"--- Script {idx+1} ---")
        print(s[:1000])
    b.close()
