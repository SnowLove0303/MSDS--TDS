# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=online&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(3000)
    
    # 查找是否有生成 canvas 或 页面层
    page.screenshot(path="openstd_preview_capture.png")
    print("Saved preview screenshot.")
    
    # 查看当前页面所有的 canvas 或者 div 结构
    structure = page.evaluate('''() => {
        return {
            htmlLen: document.body.innerHTML.length,
            childrenTags: Array.from(document.body.children).map(c => c.tagName + '.' + c.className)
        };
    }''')
    print("Structure:", structure)
    b.close()
