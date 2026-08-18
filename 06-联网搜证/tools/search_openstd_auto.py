# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import re, time, json
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

STD_QUERIES = [
    {"q": "15258-2009", "name": "化学品安全标签编写规定", "dir": "SDS框架"},
    {"q": "13690-2009", "name": "化学品分类和危险性公示 通则", "dir": "SDS框架"},
    {"q": "15603-2022", "name": "危险化学品仓库储存通则", "dir": "储存消防"},
    {"q": "12158-2006", "name": "防止静电事故通用导则", "dir": "储存消防"},
    {"q": "50016-2014", "name": "建筑设计防火规范", "dir": "储存消防"},
    {"q": "50140-2005", "name": "建筑灭火器配置设计规范", "dir": "储存消防"},
    {"q": "2890-2009", "name": "呼吸防护 自吸过滤式防毒面具", "dir": "职业卫生"},
    {"q": "2626-2019", "name": "呼吸防护 自吸过滤式防颗粒物呼吸器", "dir": "职业卫生"},
    {"q": "18664-2002", "name": "呼吸防护用品的选择、使用与维护", "dir": "职业卫生"},
    {"q": "50483-2019", "name": "化工建设项目环境保护设计标准", "dir": "环保与危废"},
    {"q": "18597-2023", "name": "危险废物贮存污染控制标准", "dir": "环保与危废"},
    {"q": "18484-2020", "name": "危险废物焚烧污染控制标准", "dir": "环保与危废"},
    {"q": "21844-2008", "name": "化学品 闪点测定 快速平衡闭杯法", "dir": "理化与毒理测试"},
    {"q": "21853-2008", "name": "化学品 沸点测定", "dir": "理化与毒理测试"},
    {"q": "21845-2008", "name": "化学品 水溶解度测定", "dir": "理化与毒理测试"},
    {"q": "21578-2008", "name": "危险品 反应性试验方法", "dir": "理化与毒理测试"},
    {"q": "21807-2008", "name": "化学品 鱼类急性毒性试验", "dir": "生态毒理测试"},
    {"q": "21809-2008", "name": "化学品 溞类急性活动抑制试验", "dir": "生态毒理测试"},
    {"q": "21805-2008", "name": "化学品 淡水藻生长抑制试验", "dir": "生态毒理测试"}
]

def search_openstd():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        page = b.new_page()
        page.goto('https://openstd.samr.gov.cn/bzgk/gb/std_list', timeout=30000)
        page.wait_for_timeout(2000)
        
        results = []
        for item in STD_QUERIES:
            q = item["q"]
            print(f"\n[Query] {q}...")
            page.fill("input[name='search1']", q)
            page.click("button#search1")
            page.wait_for_timeout(2500)
            
            rows = page.evaluate('''() => {
                const trs = document.querySelectorAll('table tbody tr');
                return Array.from(trs).map(tr => {
                    const tds = tr.querySelectorAll('td');
                    if (tds.length < 5) return null;
                    const a = tr.querySelector('a');
                    return {
                        std: tds[1] ? tds[1].innerText.trim() : '',
                        name: tds[2] ? tds[2].innerText.trim() : '',
                        status: tds[4] ? tds[4].innerText.trim() : '',
                        href: a ? a.href : ''
                    };
                }).filter(Boolean);
            }''')
            print(f"  Found {len(rows)} rows:")
            matched = False
            for r in rows:
                m = re.search(r'hcno=([A-Fa-f0-9]+)', r['href'])
                hcno = m.group(1) if m else ''
                print(f"    {r['std']} | {r['name']} | {r['status']} | HCNO: {hcno}")
                if hcno and (q in r['std'] or item['name'][:4] in r['name']) and not matched:
                    results.append({
                        "std": r['std'],
                        "name": r['name'],
                        "hcno": hcno,
                        "dir": item["dir"]
                    })
                    matched = True
            time.sleep(0.5)
        b.close()
        
        out_json = Path('F:/正式项目与模块化内容/冠志/MSDS/Word 覆写模块/数据库与推断引擎/法规匹配库/tools/new_std_hcno.json')
        out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\nSaved {len(results)} entries to {out_json}")

if __name__ == '__main__':
    search_openstd()
