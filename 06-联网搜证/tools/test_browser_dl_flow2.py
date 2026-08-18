# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(accept_downloads=True)
    page = context.new_page()
    page.goto("https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4D487D68BF0BD87E68CE0EA68183DAD6", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找所有包含下载的元素
    btn_info = page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button, a, input, div, span')).filter(el => (el.innerText || '').includes('下载') || (el.className || '').includes('xz_btn'));
        return btns.map(b => ({
            tag: b.tagName,
            class: b.className,
            text: b.innerText.trim(),
            onclick: b.getAttribute('onclick') || ''
        }));
    }''')
    print("Download buttons on newGbInfo:", btn_info)
    b.close()
