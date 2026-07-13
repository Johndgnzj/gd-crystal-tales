#!/usr/bin/env python3
"""主角外型重製 v6：LPC 圖層重捏路德（皮甲+乳白襯衣+紅披風+護腕+亮栗亂髮）與
   瑪琳（白上衣+深藍裙+短靴+暖赭馬尾）。輸出 36 幀/人到 assets/char/（覆蓋）。"""
from PIL import Image

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ  = os.path.dirname(_HERE)
GDROOT = os.path.dirname(os.path.dirname(PROJ))
LPC = f"{GDROOT}/tools/lpc/spritesheets"
A = f"{PROJ}/assets/char"
ROWS = ["Up", "Left", "Down", "Right"]

def tint(img, color):
    if color is None: return img
    r, g, b = color
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            pr, pg, pb, pa = px[x, y]
            if pa:
                px[x, y] = (pr * r // 255, pg * g // 255, pb * b // 255, pa)
    return img

def compose(layers):
    base = Image.new("RGBA", (576, 256), (0, 0, 0, 0))
    for rel, color in layers:
        img = Image.open(f"{LPC}/{rel}").convert("RGBA")
        base.alpha_composite(tint(img, color))
    return base

def export(cid, sheet):
    for r, dname in enumerate(ROWS):
        for c in range(9):
            fr = sheet.crop((c * 64, r * 64, c * 64 + 64, r * 64 + 64))
            fr.save(f"{A}/{cid}_{dname}_{c}.png")

# ---- 路德：紅披風＝英雄識別；皮甲+乳白袖+護腕；亮栗色亂髮 ----
LUDO = [
    ("cape/solid/bg/walk.png", (168, 58, 44)),
    ("body/bodies/male/walk.png", None),
    ("head/heads/human/male/walk.png", None),
    ("legs/pants/male/walk.png", (74, 84, 54)),
    ("feet/boots/rimmed/male/walk.png", (104, 74, 48)),
    ("torso/clothes/longsleeve/longsleeve/male/walk.png", (228, 218, 196)),
    ("torso/armour/leather/male/walk.png", None),
    ("arms/bracers/male/walk.png", (112, 82, 58)),
    ("cape/solid/fg/walk.png", (168, 58, 44)),
    ("hair/messy1/adult/walk.png", (108, 70, 38)),
]
# ---- 瑪琳：白上衣+深藍裙+短靴+暖赭馬尾（bg 馬尾配 bangs 前髮）----
MARIN = [
    ("hair/ponytail/adult/bg/walk.png", (176, 92, 52)),
    ("body/bodies/female/walk.png", None),
    ("head/heads/human/female/walk.png", None),
    ("legs/skirts/plain/thin/walk.png", (72, 92, 148)),
    ("feet/boots/rimmed/thin/walk.png", (118, 84, 58)),
    ("torso/clothes/blouse/female/walk/white.png", None),
    ("arms/bracers/thin/walk.png", (122, 92, 64)),
    ("hair/bangs/adult/walk.png", (176, 92, 52)),
]
export("ludo", compose(LUDO))
export("marin", compose(MARIN))
print("chars v6 done")
