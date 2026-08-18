# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import re, time

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    page = b.new_page()
    page.goto('https://openstd.samr.gov.cn/bzgk/gb/std_list', timeout=30000)
    page.wait_for_timeout(2000)
    
    for q in ["15603", "12158", "50016", "50140", "2890", "2626", "18664", "50483", "18597", "18484", "21844"]:
        page.fill("input[name='search1']", q)
        page.click("button#search1")
        page.wait_for_timeout(2000)
        
        items = page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a[onclick*="showInfo"]'));
            const list = [];
            for (let i = 0; i < links.length; i += 2) {
                const a_std = links[i];
                const a_name = links[i+1] || a_std;
                const oc = a_std.getAttribute('onclick') || '';
                const m = oc.match(/showInfo\\('([A-Fa-f0-9]+)'\\)/);
                if (m) {
                    list.push({
                        std: a_std.innerText.trim(),
                        name: a_name.innerText.trim(),
                        hcno: m[1]
                    });
                }
            }
            return list;
        }''')
        print(f"Query: {q} -> Found {len(items)} items:")
        for it in items[:2]:
            print(f"  {it['std']} | {it['name']} | HCNO: {it['hcno']}")
    b.close()
