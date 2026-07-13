#!/usr/bin/env python3
"""NPC 走路循環 v10：為戶外遊走 NPC 合成完整 LPC 走路圖（36 幀/人，覆蓋原本只有 idle 的 4 幀）。
   目的＝修「NPC 用浮的、沒有走路動畫」的 bug——遊走時 setAnimationName("Walk<dir>") 要有幀可播。
   對象：gray（老葛雷，白鬚+皮帽的老人）、guard（羅素隊長，鎖甲+鎖甲頭套的士兵）。
   villager（米拉沿用）已有 36 幀，不動。輸出到 assets/char/，須在 build_cq2.py 之前跑。"""
from PIL import Image

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ  = os.path.dirname(_HERE)
GDROOT = os.path.dirname(os.path.dirname(PROJ))
LPC = f"{GDROOT}/tools/lpc/spritesheets"
A = f"{PROJ}/assets/char"
ROWS = ["Up", "Left", "Down", "Right"]   # LPC walk 圖列序＝與 art_v6 一致

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

def whiten(img, lo=150, hi=246):
    """把（棕色）鬍鬚依原本明暗重映射成銀白漸層——multiply tint 無法提亮，故走亮度重映射。"""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                L = (r * 30 + g * 59 + b * 11) // 100
                v = lo + (hi - lo) * L // 255
                px[x, y] = (v, v, min(255, v + 4), a)
    return img

def compose(layers):
    """layers: (rel, transform)；transform 可為 None／RGB tuple(multiply)／callable。"""
    base = None
    imgs = []
    for rel, tr in layers:
        im = Image.open(f"{LPC}/{rel}").convert("RGBA")
        if callable(tr): im = tr(im)
        elif tr is not None: im = tint(im, tr)
        imgs.append(im)
    W = max(im.width for im in imgs); H = max(im.height for im in imgs)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for im in imgs: base.alpha_composite(im)
    return base

def export(cid, sheet):
    for r, dname in enumerate(ROWS):
        for c in range(9):
            fr = sheet.crop((c * 64, r * 64, c * 64 + 64, r * 64 + 64))
            fr.save(f"{A}/{cid}_{dname}_{c}.png")

# ---- 老葛雷：白鬚老人、棕皮帽、灰藍長袖、深色長褲 ----
GRAY = [
    ("body/bodies/male/walk.png", None),
    ("head/heads/human/male/walk.png", None),
    ("hair/plain/adult/walk.png", (176, 176, 172)),
    ("legs/pants/male/walk.png", (74, 72, 80)),
    ("feet/boots/rimmed/male/walk.png", (96, 72, 50)),
    ("torso/clothes/longsleeve/longsleeve/male/walk.png", (138, 146, 150)),
    ("beards/beard/basic/walk.png", whiten),
    ("hat/cloth/leather_cap/adult/walk.png", (110, 80, 54)),
]
# ---- 羅素隊長：鎖甲＋鎖甲頭套的守衛 ----
GUARD = [
    ("body/bodies/male/walk.png", None),
    ("head/heads/human/male/walk.png", None),
    ("legs/pants/male/walk.png", (60, 60, 70)),
    ("feet/boots/rimmed/male/walk.png", (82, 82, 90)),
    ("torso/chainmail/male/walk.png", (206, 210, 220)),
    ("hat/helmet/mail/adult/walk.png", (206, 210, 220)),
]
export("gray", compose(GRAY))
export("guard", compose(GUARD))
print("npc walk v10 done: gray, guard (36 frames each)")
