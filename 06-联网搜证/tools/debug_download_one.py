# -*- coding: utf-8 -*-
"""单步调试 openstd PDF 下载过程"""
import requests, ddddocr, time
from pathlib import Path

BASE = "https://openstd.samr.gov.cn/bzgk/std"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

ocr = ddddocr.DdddOcr(show_ad=False)

def download_one(hcno, filename):
    print(f"\n--- 下载测试: {filename} (HCNO: {hcno}) ---")
    s = requests.Session()
    s.headers.update(HEADERS)
    
    # 1. 打开下载页面
    url_show = f"{BASE}/showGb?type=download&hcno={hcno}"
    r_show = s.get(url_show, timeout=20)
    print("1. 打开 showGb:", r_show.status_code)
    
    # 2. 识别验证码
    for attempt in range(5):
        gc_url = f"{BASE}/gc?_{int(time.time()*1000)}"
        r_gc = s.get(gc_url, timeout=15)
        print(f"2. 获取验证码(尝试 {attempt+1}):", r_gc.status_code, f"大小: {len(r_gc.content)}")
        if r_gc.status_code != 200 or len(r_gc.content) < 500:
            time.sleep(1)
            continue
            
        code = ocr.classification(r_gc.content).strip()
        print(f"   OCR 识别结果: '{code}' (长度 {len(code)})")
        if len(code) != 4:
            time.sleep(1)
            continue
            
        r_verify = s.post(f"{BASE}/verifyCode", data={"verifyCode": code}, timeout=15)
        print("3. verifyCode 返回:", r_verify.status_code, f"'{r_verify.text.strip()}'")
        
        if r_verify.text.strip() == "success":
            print("4. 验证码通过，准备请求 viewGb 生成并拉取 PDF...")
            for wait_idx in range(6):
                time.sleep(2)
                r_pdf = s.get(f"{BASE}/viewGb?hcno={hcno}", timeout=60)
                print(f"   拉取 viewGb (第 {wait_idx+1} 次):", r_pdf.status_code, f"大小: {len(r_pdf.content)}")
                if r_pdf.status_code == 200 and len(r_pdf.content) > 2000:
                    out = Path(filename)
                    out.write_bytes(r_pdf.content)
                    print(f"✅ 下载成功! 保存为 {filename} ({len(r_pdf.content)} 字节)")
                    return True
            print("❌ viewGb 拉取超时或内容为空")
            return False
        time.sleep(1)
    return False

if __name__ == '__main__':
    download_one("4D487D68BF0BD87E68CE0EA68183DAD6", "GB_15258-2009.pdf")
