# -*- coding: utf-8 -*-
"""下载全部匹配到的 GB 强制性标准 PDF."""
import sys, time, json, re
from pathlib import Path
import requests, ddddocr

BASE = "https://openstd.samr.gov.cn/bzgk/std"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

ROOT_OUT = Path(r"F:\正式项目与模块化内容\冠志\MSDS\Word 覆写模块\数据库与推断引擎\法规匹配库\标准原文归档")

STANDARDS = [
    {"std": "GB 15258-2009", "name": "化学品安全标签编写规定", "hcno": "4D487D68BF0BD87E68CE0EA68183DAD6", "dir": "SDS框架"},
    {"std": "GB 13690-2009", "name": "化学品分类和危险性公示 通则", "hcno": "3838CDBD0DCE4ECDDB29626DAB24F1D2", "dir": "SDS框架"},
    {"std": "GB 15603-2022", "name": "危险化学品仓库储存通则", "hcno": "4BB90BF6C7015DF7E4905694A80F7C57", "dir": "储存消防"},
    {"std": "GB 12158-2006", "name": "防止静电事故通用导则", "hcno": "72044654B474A33FE699AAA229BC4331", "dir": "储存消防"},
    {"std": "GB 2890-2009", "name": "呼吸防护 自吸过滤式防毒面具", "hcno": "CA5496664BB4FE051F65DC9A1843B8BE", "dir": "职业卫生"},
    {"std": "GB 18597-2023", "name": "危险废物贮存污染控制标准", "hcno": "ABC96AD5640339CA228C384D6843CDEF", "dir": "环保与危废"},
    {"std": "GB 18484-2020", "name": "危险废物焚烧污染控制标准", "hcno": "CCF2DECFB52B87E9C5439D613E44BDF7", "dir": "环保与危废"},
    {"std": "GB-T 21844-2008", "name": "化合物(蒸气和气体)易燃性浓度限值的标准试验方法", "hcno": "C39DC7501629C28A594245E8259ED04F", "dir": "理化与毒理测试"},
    {"std": "GB-T 21853-2008", "name": "化学品 分配系数（正辛醇-水） 摇瓶法试验", "hcno": "62D5B72E64ECC84A8EEBBE2FA790B8F4", "dir": "理化与毒理测试"},
    {"std": "GB-T 21845-2008", "name": "化学品 水溶解度试验", "hcno": "89FA298DED2591D5B5CD7834A19B161D", "dir": "理化与毒理测试"},
    {"std": "GB-T 21578-2008", "name": "危险品 克南试验方法", "hcno": "CBC7A76A2FAA05A0298D7FFD1933C60A", "dir": "理化与毒理测试"},
    {"std": "GB-T 21807-2008", "name": "化学品 鱼类胚胎和卵黄囊仔鱼阶段的短期毒性试验", "hcno": "89813B717B499B8D77B04EBF94911EC0", "dir": "生态毒理测试"},
    {"std": "GB-T 21809-2008", "name": "化学品 蚯蚓急性毒性试验", "hcno": "2E47E6B758B6CBAF263F762DAA96C441", "dir": "生态毒理测试"},
    {"std": "GB-T 21805-2008", "name": "化学品 藻类生长抑制试验", "hcno": "8E7F11A9A3A2D8689BE7DC8332F6CB3F", "dir": "生态毒理测试"}
]

def fetch_std(hcno, out_path, ocr, rounds=3):
    out = Path(out_path)
    if out.exists() and out.stat().st_size > 1000:
        return ("skip", {"size": out.stat().st_size})
    for rnd in range(rounds):
        s = requests.Session()
        h = dict(HEADERS)
        h["Referer"] = f"{BASE}/showGb?type=download&hcno={hcno}"
        s.headers.update(h)
        try:
            s.get(f"{BASE}/showGb?type=download&hcno={hcno}", timeout=25)
        except Exception:
            time.sleep(2); continue
        for i in range(5):
            try:
                r = s.get(f"{BASE}/gc?_{int(time.time()*1000)}", timeout=25)
                if r.status_code != 200 or len(r.content) < 500:
                    continue
                code = ocr.classification(r.content).strip()
                if len(code) != 4:
                    continue
                rv = s.post(f"{BASE}/verifyCode", data={"verifyCode": code}, timeout=25)
                if rv.text.strip() == "success":
                    for k in range(8):
                        time.sleep(1.5)
                        rd = s.get(f"{BASE}/viewGb?hcno={hcno}", timeout=120)
                        if rd.status_code == 200 and len(rd.content) > 1000:
                            out.parent.mkdir(parents=True, exist_ok=True)
                            out.write_bytes(rd.content)
                            return ("ok", {"round": rnd+1, "code": code, "size": len(rd.content)})
                    break
            except Exception:
                time.sleep(1)
    return ("fail", {})

def main():
    ocr = ddddocr.DdddOcr(show_ad=False)
    ok = skip = fail = 0
    for it in STANDARDS:
        std = it["std"]
        name = it["name"]
        hcno = it["hcno"]
        subdir = it["dir"]
        dest = ROOT_OUT / subdir / f"{std}.pdf"
        print(f"\n[下载中] {std} - {name}...")
        st, info = fetch_std(hcno, dest, ocr)
        if st == "ok":
            ok += 1
            print(f"  ✅ 成功! 大小: {info['size']} 字节")
        elif st == "skip":
            skip += 1
            print(f"  ⏭ 已存在 ({info['size']} 字节)")
        else:
            fail += 1
            print(f"  ❌ 失败")
        time.sleep(0.5)
    print(f"\n下载汇总: 成功 {ok} | 已存在 {skip} | 失败 {fail}")

if __name__ == '__main__':
    main()
