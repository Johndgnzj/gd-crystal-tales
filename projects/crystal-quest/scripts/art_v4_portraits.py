#!/usr/bin/env python3
"""對話立繪：路德/瑪琳/亞倫 48px 像素半身像 → 3x 放大（144x144）。
   風格依 ART_PROMPTS：16-bit JRPG、有限調色盤、乾淨像素。"""
from PIL import Image, ImageDraw

A = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/projects/crystal-quest/assets"
S = 48  # 邏輯畫布

def px(d, x, y, c):
    if 0 <= x < S and 0 <= y < S: d.point((x, y), fill=c)

def hline(d, x1, x2, y, c): d.line([(x1, y), (x2, y)], fill=c)

def make_bust(skin, skin_sh, skin_hi, eye, hair, hair_sh, hair_hi, cloth, cloth_sh, collar,
              hair_fn, extras_fn=None, brow_y=17, mouth="smile", jaw=0):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (34, 28, 36)          # 深色描邊
    cx = 24
    # ---- 肩膀/衣服 ----
    d.polygon([(8, 47), (10, 38), (15, 34), (33, 34), (38, 38), (40, 47)], fill=cloth, outline=OUT)
    d.line([(10, 40), (14, 36)], fill=cloth_sh); d.line([(34, 36), (38, 40)], fill=cloth_sh)
    hline(d, 12, 36, 46, cloth_sh)
    # 領口
    d.polygon([(18, 34), (30, 34), (27, 40), (21, 40)], fill=collar, outline=OUT)
    # ---- 脖子 ----
    d.rectangle([20, 29, 27, 35], fill=skin, outline=None)
    hline(d, 20, 27, 33, skin_sh)
    # ---- 臉（含下顎收窄）----
    d.rectangle([14, 12, 33, 24], fill=skin)                      # 上半臉
    d.polygon([(14, 24), (33, 24), (31 - jaw, 29), (26, 31), (21, 31), (16 + jaw, 29)], fill=skin)
    # 臉部立體感
    d.line([(14, 13), (14, 23)], fill=skin_sh)                    # 左緣影
    d.line([(33, 13), (33, 23)], fill=skin_hi)
    hline(d, 17 + jaw, 30 - jaw, 30, skin_sh)                     # 下顎影
    # 外輪廓描邊
    d.line([(13, 12), (13, 24), (15 + jaw, 29), (20, 32), (27, 32), (32 - jaw, 29), (34, 24), (34, 12)], fill=OUT, joint="curve")
    # ---- 五官 ----
    for ex in (17, 27):                                            # 眼（2x3 + 高光）
        d.rectangle([ex, 19, ex + 3, 21], fill=(246, 246, 250))
        d.rectangle([ex + 1, 19, ex + 2, 21], fill=eye)
        px(d, ex + 1, 19, (255, 255, 255))
        hline(d, ex, ex + 3, 18, OUT)                              # 上眼線
    hline(d, 16, 20, brow_y, hair_sh)                              # 眉
    hline(d, 27, 31, brow_y, hair_sh)
    px(d, 23, 24, skin_sh); px(d, 24, 25, skin_sh)                 # 鼻
    if mouth == "smile":
        hline(d, 21, 26, 28, (150, 80, 74)); px(d, 20, 27, (150, 80, 74)); px(d, 27, 27, (150, 80, 74))
    elif mouth == "calm":
        hline(d, 21, 26, 28, (150, 80, 74))
    else:  # stern
        hline(d, 20, 26, 28, (110, 62, 58))
    px(d, 16, 25, (232, 150, 140)); px(d, 31, 25, (232, 150, 140))  # 腮紅點
    # ---- 髮型（角色自訂函式）----
    hair_fn(d, hair, hair_sh, hair_hi, OUT)
    if extras_fn: extras_fn(d, OUT)
    return im

# ============ 路德：深棕短亂髮・旅行者皮革（棕綠） ============
def hair_ludo(d, h, hs, hh, OUT):
    d.polygon([(11, 14), (12, 8), (16, 4), (24, 3), (31, 4), (35, 8), (36, 14), (34, 12),
               (33, 15), (30, 10), (26, 13), (21, 9), (17, 13), (14, 10), (13, 16)], fill=h, outline=OUT)
    # 亂翹髮束
    for sx, sy in [(10, 10), (36, 9), (20, 2), (29, 2)]:
        d.line([(sx, sy), (sx + 2, sy + 3)], fill=h)
    d.line([(15, 6), (22, 4)], fill=hh); d.line([(26, 4), (32, 7)], fill=hh)
    d.line([(13, 14), (15, 15)], fill=hs); d.line([(33, 13), (35, 14)], fill=hs)
    # 鬢角
    d.line([(13, 15), (13, 19)], fill=h); d.line([(34, 15), (34, 19)], fill=h)
def extra_ludo(d, OUT):
    d.polygon([(9, 38), (13, 34), (15, 40), (12, 47)], fill=(168, 58, 44))   # 紅披風垂布
    d.line([(13, 34), (18, 35)], fill=(140, 44, 34))                          # 披風繫帶
    d.line([(15, 35), (26, 46)], fill=(126, 92, 56), width=2)                 # 皮革斜背帶
    d.point((20, 40), fill=(196, 172, 120))

# ============ 瑪琳：紅棕馬尾＋瀏海・輕便旅裝 ============
def hair_marin(d, h, hs, hh, OUT):
    d.polygon([(12, 16), (12, 8), (17, 4), (24, 3), (31, 4), (36, 8), (36, 16), (34, 11),
               (30, 13), (27, 8), (24, 12), (20, 8), (16, 13), (14, 11)], fill=h, outline=OUT)
    d.polygon([(33, 8), (39, 6), (41, 12), (42, 22), (40, 30), (37, 25), (38, 14), (36, 10)], fill=h, outline=OUT)  # 馬尾
    d.line([(39, 10), (40, 20)], fill=hs)
    d.line([(17, 6), (23, 4)], fill=hh); d.line([(27, 4), (33, 7)], fill=hh)
    d.line([(14, 12), (16, 14)], fill=hs)
    d.line([(13, 16), (13, 21)], fill=h); d.line([(34, 15), (34, 20)], fill=h)  # 側髮
    d.point((37, 9), fill=(226, 196, 116))                          # 髮圈
def extra_marin(d, OUT):
    d.line([(18, 34), (21, 40)], fill=(238, 234, 224))              # 白襯領
    d.line([(30, 34), (27, 40)], fill=(238, 234, 224))

# ============ 亞倫：黑髮風霜・深色重裝・疤 ============
def hair_aaron(d, h, hs, hh, OUT):
    d.polygon([(12, 15), (13, 7), (18, 4), (25, 3), (32, 5), (35, 9), (35, 15), (32, 11),
               (28, 13), (23, 9), (18, 12), (15, 10), (14, 16)], fill=h, outline=OUT)
    d.line([(16, 6), (22, 4)], fill=hh)
    d.line([(31, 7), (34, 12)], fill=(150, 150, 158))               # 灰白髮線
    d.line([(14, 9), (16, 12)], fill=(150, 150, 158))
    d.line([(13, 15), (13, 20)], fill=h); d.line([(34, 15), (34, 20)], fill=h)
def extra_aaron(d, OUT):
    d.line([(28, 14), (31, 18)], fill=(176, 120, 108))              # 右頰疤
    for yy in range(25, 31, 2): d.point((18, yy), fill=(90, 84, 92))  # 鬍渣
    for yy in range(26, 31, 2): d.point((29, yy), fill=(90, 84, 92))
    d.rectangle([8, 36, 14, 42], fill=(96, 100, 112), outline=OUT)   # 左肩甲
    d.rectangle([34, 36, 40, 42], fill=(96, 100, 112), outline=OUT)
    d.line([(9, 37), (13, 37)], fill=(150, 156, 170))

CHARS = {
 "ludo":  dict(skin=(236, 188, 148), skin_sh=(206, 152, 112), skin_hi=(246, 206, 170), eye=(150, 96, 40),
               hair=(100, 66, 38), hair_sh=(70, 45, 26), hair_hi=(134, 92, 54),
               cloth=(142, 100, 60), cloth_sh=(110, 76, 44), collar=(228, 218, 196),
               hair_fn=hair_ludo, extras_fn=extra_ludo, mouth="smile"),
 "marin": dict(skin=(242, 198, 162), skin_sh=(212, 162, 126), skin_hi=(250, 214, 180), eye=(60, 130, 84),
               hair=(170, 90, 52), hair_sh=(126, 62, 38), hair_hi=(204, 122, 74),
               cloth=(236, 232, 224), cloth_sh=(200, 196, 186), collar=(88, 106, 152),
               hair_fn=hair_marin, extras_fn=extra_marin, mouth="calm"),
 "aaron": dict(skin=(220, 170, 132), skin_sh=(186, 134, 100), skin_hi=(232, 186, 150), eye=(88, 110, 140),
               hair=(50, 48, 56), hair_sh=(32, 30, 38), hair_hi=(78, 76, 88),
               cloth=(70, 74, 86), cloth_sh=(52, 56, 66), collar=(96, 100, 112),
               hair_fn=hair_aaron, extras_fn=extra_aaron, mouth="stern", brow_y=16, jaw=1),
}
for cid, p in CHARS.items():
    im = make_bust(**p)
    im = im.resize((S * 3, S * 3), Image.NEAREST)
    im.save(f"{A}/ui/face_{cid}.png")
print("portraits done")
