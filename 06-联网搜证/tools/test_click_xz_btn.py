# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "BD4BA33D46B2AD5DCA3F1EBA7E99BEE6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=download&hcno={hcno}", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 点击 .xz_btn
    page.click('.xz_btn')
    page.wait_for_timeout(2000)
    
    # 查找是否有弹出模态框或验证码
    modal = page.evaluate('''() => {
        const m = document.querySelector('.modal, #myModal, .modal-dialog');
        return m ? m.innerHTML : 'NO_MODAL';
    }''')
    print("Modal HTML:\n", modal[:1000])
    b.close()
