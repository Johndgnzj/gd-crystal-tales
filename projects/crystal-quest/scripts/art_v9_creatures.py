#!/usr/bin/env python3
"""LPC 生物敵人（非人形）v9：從 OGA LPC 相容生物 spritesheet（tools/lpc-creatures/）裁正面戰鬥幀，
輸出到 assets/battle/lpc_src/<sprite>_0.png（build 的 LPC_FOES 讀取）。
素材授權見 CREDITS：[LPC] Monsters(CC-BY-SA/GPL)、[LPC] Wolf Animation / bears / Imp2(CC-BY)、[LPC] Birds(CC-BY)。
執行序：art_v8_foes.py + art_v9_creatures.py → build_cq2.py → art_v2 → art_v3"""
import os
from PIL import Image

SRC = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/tools/lpc-creatures"
OUT = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/projects/crystal-quest/assets/battle/lpc_src"
os.makedirs(OUT, exist_ok=True)

def largest_blob(img):
    """保留最大連通（非透明）區塊——用來從密集堆疊的表中只取出一隻。"""
    px = img.load(); W, H = img.size
    seen = [[False]*W for _ in range(H)]; best = None; bestn = 0
    for sy in range(H):
        for sx in range(W):
            if seen[sy][sx] or px[sx, sy][3] == 0: continue
            stack = [(sx, sy)]; seen[sy][sx] = True; comp = []
            while stack:
                cx, cy = stack.pop(); comp.append((cx, cy))
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = cx+dx, cy+dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and px[nx, ny][3] > 0:
                        seen[ny][nx] = True; stack.append((nx, ny))
            if len(comp) > bestn: bestn = len(comp); best = comp
    if not best: return img
    xs = [c[0] for c in best]; ys = [c[1] for c in best]
    x0, x1, y0, y1 = min(xs), max(xs)+1, min(ys), max(ys)+1
    out = Image.new("RGBA", (x1-x0, y1-y0), (0,0,0,0)); op = out.load()
    for cx, cy in best: op[cx-x0, cy-y0] = px[cx, cy]
    return out

def tint(img, color):
    if color is None: return img
    r, g, b = color; px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            pr, pg, pb, pa = px[x, y]
            if pa: px[x, y] = (pr*r//255, pg*g//255, pb*b//255, pa)
    return img

# sprite: (檔案, 裁切框, 放大, 染色, 水平翻轉, 只取最大連通塊)  Down 列(row2)=y128-192 面向鏡頭
REC = {
 "gslime": ("slime.png",        (0,128,64,192), 1.0, None, False, False),
 "worm":   ("big_worm.png",     (0,128,64,192), 1.0, None, False, False),
 "wogol":  ("bat.png",          (128,128,192,192),1.1, None, False, False),   # Down 列 frame2＝翅展較明顯
 "demon":  ("ghost.png",        (0,128,64,192), 1.7, None, False, False),      # 魔影＝Boss，放大
 "chort":  ("imp_green_walk.png",(0,128,64,192),1.0, (150,120,190), False, False), # 暗影小魔＝紫調
 "bird":   ("bird_eagle.png",   (0,128,32,160), 1.4, None, False, False),      # 單格 32×32 一隻鷹
 "bear":   ("bear_grizzly.png", (0,128,64,192), 1.35,None, True, False),        # 側視熊，翻成面向右（朝我方）
 "wolf":   ("wolf.png",         (384,96,452,152),1.15,None, False, True),       # 側視狼；密集堆疊→取最大連通塊只留一隻
}

made = []
for sprite, (fn, box, scale, col, flip, blob) in REC.items():
    p = f"{SRC}/{fn}"
    if not os.path.exists(p): print("!! missing", fn); continue
    im = Image.open(p).convert("RGBA")
    fr = im.crop(box)
    fr = largest_blob(fr) if blob else fr.crop(fr.getbbox() or (0,0,fr.width,fr.height))
    fr = tint(fr, col)
    if flip: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    if scale != 1.0: fr = fr.resize((max(1,round(fr.width*scale)), max(1,round(fr.height*scale))), Image.NEAREST)
    fr.save(f"{OUT}/{sprite}_0.png"); made.append(f"{sprite}({fr.width}x{fr.height})")
print("art v9 creatures done:", ", ".join(made))

# 檢視用 contact sheet
ids = list(REC.keys()); S = 3; pad = 16
imgs = [Image.open(f"{OUT}/{i}_0.png") for i in ids]
W = sum(im.width*S+pad for im in imgs)+pad; H = max(im.height for im in imgs)*S+50
from PIL import ImageDraw
sheet = Image.new("RGBA", (W, H), (70,74,86,255)); dr = ImageDraw.Draw(sheet); x = pad
for i, im in zip(ids, imgs):
    big = im.resize((im.width*S, im.height*S), Image.NEAREST); y = H-24-big.height
    sheet.alpha_composite(big, (x, y)); dr.text((x, 8), i, fill=(255,255,255,255)); x += big.width+pad
sheet.convert("RGB").save("/private/tmp/claude-501/-Users-john-Projects-60-soho-30-Personal-GameCreator-GDevelop/910255e6-39e9-4588-9fb8-745ee52a8464/scratchpad/creatures_sheet.png")
print("contact sheet saved")
