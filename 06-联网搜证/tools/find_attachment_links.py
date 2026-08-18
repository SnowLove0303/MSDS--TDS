# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import requests
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
url = "https://www.so.com/link?m=eVdLevyhQq7qZBk1yEXL%2BrJHhaF8Apf6nWaipTdUXkH6ukZKsBzJGYRCISez9YdC8yBvraz%2BLVwC0WTgVg%2BNnJkKMrHaq88tIJ53Bj2IA%2BXyo6JIuxlTtCpzC5wMLSikSiAfzoY49EEc3%2Bt1crUJZ0hGjmP3XWLHcaGkuUYd8m%2BH%2FDY2k2lC6Z0eXOxuP%2BjdQRZ4Ert%2F99ACZLalctzlJMGIhasIGmEvhQvYSffFgRJYRvEAMog7GfOhPGm2kknjYbUF%2BD2A7gXL89lkMeiJO4s4TcWTfd%2BXnt7uM9jQRaiqq4bahmA7CKc0Lcvc%3D"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(url, timeout=30000)
    page.wait_for_timeout(2000)
    
    # 查找页面中包含附件的 a 标签
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => [(a.innerText || '').trim(), a.href]);
    }''')
    for l in links:
        if '附件' in l[0] or 'doc' in l[0] or '名录' in l[0] or 'download' in l[1] or 'system' in l[1]:
            print("Found target link:", l)
            if l[1].startswith('http'):
                r = requests.get(l[1], headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
                if len(r.content) > 1000:
                    out = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库与推断引擎\法规匹配库\法规原文归档\目录公告\易制爆危险化学品名录（2017年版）.doc")
                    out.write_bytes(r.content)
                    print(f"✅ 成功下载附件! 大小: {len(r.content)} 字节")
                    break
    b.close()
