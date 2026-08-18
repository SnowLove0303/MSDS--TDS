# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import re, time, json
from pathlib import Path

CHROME = r'E:\MorenAnzhuangLujing\Chrome\Chrome\Application\chrome.exe'

STD_LIST = [
    # 强制与推荐
    {"q": "15258", "dir": "SDS框架", "name": "GB 15258-2009 化学品安全标签编写规定"},
    {"q": "13690", "dir": "SDS框架", "name": "GB 13690-2009 化学品分类和危险性公示 通则"},
    {"q": "15603", "dir": "储存消防", "name": "GB 15603-2022 危险化学品仓库储存通则"},
    {"q": "12158", "dir": "储存消防", "name": "GB 12158-2006 防止静电事故通用导则"},
    {"q": "50016", "dir": "储存消防", "name": "GB 50016-2014(2018) 建筑设计防火规范"},
    {"q": "50140", "dir": "储存消防", "name": "GB 50140-2005 建筑灭火器配置设计规范"},
    {"q": "2890", "dir": "职业卫生", "name": "GB 2890-2009 呼吸防护 自吸过滤式防毒面具"},
    {"q": "2626", "dir": "职业卫生", "name": "GB 2626-2019 呼吸防护 自吸过滤式防颗粒物呼吸器"},
    {"q": "18664", "dir": "职业卫生", "name": "GB/T 18664-2002 呼吸防护用品的选择、使用与维护"},
    {"q": "50483", "dir": "环保与危废", "name": "GB 50483-2019 化工建设项目环境保护设计标准"},
    {"q": "18597", "dir": "环保与危废", "name": "GB 18597-2023 危险废物贮存污染控制标准"},
    {"q": "18484", "dir": "环保与危废", "name": "GB 18484-2020 危险废物焚烧污染控制标准"},
    {"q": "21844", "dir": "理化与毒理测试", "name": "GB/T 21844-2008 闪点测定 快速平衡闭杯法"},
    {"q": "21853", "dir": "理化与毒理测试", "name": "GB/T 21853-2008 沸点测定"},
    {"q": "21845", "dir": "理化与毒理测试", "name": "GB/T 21845-2008 水溶解度测定"},
    {"q": "21578", "dir": "理化与毒理测试", "name": "GB/T 21578-2008 危险品 反应性试验方法"},
    {"q": "21807", "dir": "生态毒理测试", "name": "GB/T 21807-2008 鱼类急性毒性试验"},
    {"q": "21809", "dir": "生态毒理测试", "name": "GB/T 21809-2008 溞类急性活动抑制试验"},
    {"q": "21805", "dir": "生态毒理测试", "name": "GB/T 21805-2008 淡水藻生长抑制试验"}
]

def search_stds():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        page = b.new_page()
        
        found_hcno = []
        for item in STD_LIST:
            q = item["q"]
            print(f"\n[Searching] {item['name']} ({q})...")
            # 搜索全部类型 (p.p1=0)
            url = f"https://openstd.samr.gov.cn/bzgk/std/std_list_type?p.p1=0&p.p2={q}"
            page.goto(url, timeout=30000)
            page.wait_for_timeout(1500)
            
            rows = page.evaluate('''() => {
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
            
            print(f"  Found {len(rows)} candidates:")
            matched = False
            for r in rows:
                print(f"    {r['std']} | {r['name']} | HCNO: {r['hcno']}")
                # 过滤出匹配的
                if not matched and q in r['std']:
                    found_hcno.append({
                        "std": r['std'],
                        "name": r['name'],
                        "hcno": r['hcno'],
                        "dir": item["dir"]
                    })
                    matched = True
            time.sleep(0.5)
        b.close()
        
        out_file = Path('F:/正式项目与模块化内容/冠志/MSDS/Word 覆写模块/数据库与推断引擎/法规匹配库/tools/found_std_hcno.json')
        out_file.write_text(json.dumps(found_hcno, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n✅ Total matched HCNOs: {len(found_hcno)} saved to {out_file}")

if __name__ == '__main__':
    search_stds()
