# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import re, time

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

def test_openstd_lookup():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        page = b.new_page()
        page.goto('https://openstd.samr.gov.cn/bzgk/gb/index', timeout=30000)
        page.wait_for_timeout(1500)
        print('Title:', page.title())
        
        # 尝试在输入框输入 15603
        for std_no in ["15603", "15258", "18597", "18484", "12158", "50016", "50140", "2890", "2626", "18664", "21844"]:
            page.fill('#query_key', std_no)
            page.click('#btn_query')
            page.wait_for_timeout(2000)
            
            # 获取结果列表里的链接
            links = page.evaluate('''() => {
                const trs = document.querySelectorAll('table tbody tr');
                return Array.from(trs).map(tr => {
                    const tds = tr.querySelectorAll('td');
                    if (tds.length < 4) return null;
                    const a = tr.querySelector('a');
                    return {
                        std: tds[1] ? tds[1].innerText.trim() : '',
                        name: tds[2] ? tds[2].innerText.trim() : '',
                        status: tds[4] ? tds[4].innerText.trim() : '',
                        href: a ? a.href : ''
                    };
                }).filter(Boolean);
            }''')
            print(f"\nQuery: {std_no} -> {len(links)} results:")
            for l in links[:3]:
                m = re.search(r'hcno=([A-Fa-f0-9]+)', l["href"])
                hcno = m.group(1) if m else "NO_HCNO"
                print(f"  {l['std']} | {l['name']} | {l['status']} | HCNO: {hcno}")
        b.close()

if __name__ == '__main__':
    test_openstd_lookup()
