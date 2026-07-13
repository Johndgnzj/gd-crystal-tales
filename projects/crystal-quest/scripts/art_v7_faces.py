#!/usr/bin/env python3
"""立繪接圖：design/faces/ 的半身生成圖（橫幅、人物置中、中性深底）→
   偵測人物水平中心 → 裁正方形 → 縮 144x144 → 覆蓋 assets/ui/face_*.png。
   只吃半身圖（<name>.png）；全身圖（<name>_full.png）不在名單、不會被裁。
   檔案不存在時保留舊版（主角三位有程式繪備援）。在 art_v4_portraits.py 之後執行。"""
import os
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(_HERE)
SRC = f"{PROJ}/design/faces"
DST = f"{PROJ}/assets/ui"
# id → 來源檔名候選（依序找；lude/alan 為 John 早期產圖的舊檔名）
FACE_SRC = {
    "ludo":   ["ludo", "lude"],
    "marin":  ["marin"],
    "aaron":  ["aaron", "alan"],
    "tina":   ["tina"],
    "dora":   ["dora"],
    "sister": ["sister"],
    "barton": ["barton"],
    "gid":    ["gid"],
    "hank":   ["hank"],
    "martha": ["martha"],
    "gray":   ["gray"],
    "mira":   ["mira"],
    "guard":  ["guard"],
}

def find_src(cid):
    if not os.path.isdir(SRC): return None
    files = {f.lower(): f for f in os.listdir(SRC)}
    for alias in FACE_SRC[cid]:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            if alias + ext in files: return f"{SRC}/{files[alias + ext]}"
    return None

def content_center_x(im):
    """以左上角當背景色，找出與背景差異大的欄位範圍中心（忽略右側小裝飾）。"""
    small = im.resize((im.width // 8, im.height // 8))
    px = small.load()
    bg = px[2, 2]
    cols = []
    for x in range(small.width):
        cnt = 0
        for y in range(small.height):
            r, g, b = px[x, y][:3]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > 60: cnt += 1
        cols.append(cnt)
    th = max(cols) * 0.2
    runs, cur = [], None
    for x, c in enumerate(cols):
        if c > th:
            if cur is None: cur = [x, x]
            else: cur[1] = x
        else:
            if cur: runs.append(cur); cur = None
    if cur: runs.append(cur)
    if not runs: return im.width // 2
    # 以區內像素總量選主體：人物稠密、星群稀疏（純寬度會被大片星星騙走）
    main = max(runs, key=lambda r: sum(cols[r[0]:r[1] + 1]))
    if (main[1] - main[0]) * 8 > im.width * 0.7:
        return im.width // 2   # 背景有漸層時偵測會併成全寬：退回「人物置中」約定
    return (main[0] + main[1]) * 8 // 2

for cid in FACE_SRC:
    src = find_src(cid)
    if not src:
        print(f"{cid}: 無生成圖，保留現有"); continue
    im = Image.open(src).convert("RGBA")
    side = im.height
    cx = content_center_x(im)
    x1 = max(0, min(im.width - side, cx - side // 2))
    sq = im.crop((x1, 0, x1 + side, side))
    sq = sq.resize((144, 144), Image.LANCZOS)
    sq.save(f"{DST}/face_{cid}.png")
    print(f"{cid}: {os.path.basename(src)} → face_{cid}.png (crop x={x1})")
