# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'
hcno = "4D487D68BF0BD87E68CE0EA68183DAD6"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    context = b.new_context()
    page = context.new_page()
    page.goto(f"https://openstd.samr.gov.cn/bzgk/std/showGb?type=online&hcno={hcno}&request_locale=zh", timeout=30000)
    page.wait_for_timeout(3000)
    
    # 查找是否有 pdf 渲染相关的元素、canvas、svg 或 text
    dom_info = page.evaluate('''() => {
        const canvases = document.querySelectorAll('canvas');
        const svgs = document.querySelectorAll('svg');
        const images = document.querySelectorAll('img');
        const iframes = document.querySelectorAll('iframe');
        const text_len = document.body.innerText.length;
        return {
            canvases: canvases.length,
            svgs: svgs.length,
            images: Array.from(images).map(i => i.src),
            iframes: Array.from(iframes).map(f => f.src),
            text_len: text_len
        };
    }''')
    print("DOM Info:", dom_info)
    
    # 打印页面 PDF 渲染容器
    container = page.evaluate('''() => {
        const div = document.querySelector('#viewer, #pdf-viewer, .page, #canvas, #content');
        return div ? div.outerHTML.substring(0, 300) : 'NO_CONTAINER';
    }''')
    print("Container:", container)
    b.close()
