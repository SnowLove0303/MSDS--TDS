# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
OUT_DIR = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库与推断引擎\法规匹配库\标准原文归档\SDS框架")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context(accept_downloads=True)
    page = context.new_page()
    page.goto("https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4D487D68BF0BD87E68CE0EA68183DAD6", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找是否有下载按钮
    print("Page title:", page.title())
    has_dl = page.evaluate('() => document.querySelector(".xz_btn, button:has-text(\'下载\')") !== null')
    print("Has download button:", has_dl)
    b.close()
