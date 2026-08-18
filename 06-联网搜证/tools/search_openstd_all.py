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

def search_all_openstd():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        page = b.new_page()
        # 使用全国标搜索入口
        page.goto('https://openstd.samr.gov.cn/bzgk/std/std_list', timeout=30000)
        page.wait_for_timeout(2000)
        
        results = []
        for item in STD_QUERIES:
            q = item["q"]
            print(f"\n[Query] {q} ({item['name']})...")
            # 勾选全部或者在输入框输入
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
                        list.append ? null : null;
                        list.push({
                            std: a_std.innerText.trim(),
                            name: a_name.innerText.trim(),
                            hcno: m[1]
                        });
                    }
                }
                return list;
            }''')
            
            print(f"  Found {len(items)} items:")
            matched = False
            for it in items:
                print(f"    {it['std']} | {it['name']} | HCNO: {it['hcno']}")
                if not matched and (q in it['std'] or item['name'][:4] in it['name']):
                    results.append({
                        "std": it['std'],
                        "name": it['name'],
                        "hcno": it['hcno'],
                        "dir": item["dir"]
                    })
                    matched = True
            time.sleep(0.5)
        b.close()
        
        out_json = Path('F:/正式项目与模块化内容/冠志/MSDS/Word 覆写模块/数据库与推断引擎/法规匹配库/tools/matched_new_stds.json')
        out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\nSaved {len(results)} matches to {out_json}")

if __name__ == '__main__':
    search_all_openstd()
