#!/usr/bin/env python3
"""戰鬥大圖 v2：每角色取 Left 行走 4 幀（踏步待機動畫），用聯集 bbox 統一裁切後
   4x 最近鄰放大 → battle/hero_<id>_f0..3.png；尺寸寫入 battle/hero_dims.json。
   另重繪指向左的目標游標 ui/cursor.png（游標顯示在目標右側）。"""
import json
from PIL import Image, ImageDraw

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ  = os.path.dirname(_HERE)
GDROOT = os.path.dirname(os.path.dirname(PROJ))
A = f"{PROJ}/assets"
LPC = f"{GDROOT}/tools/lpc/spritesheets"
FRAMES = [1, 3, 5, 7]   # 行走循環取 4 幀
LEFT_ROW = 1            # LPC walk 表第 1 列 = 面向左
# 戰鬥持武器：LPC weapon walk 圖層（fg 疊上、behind 墊下）
WEAPONS = {
    "ludo":  ("weapon/sword/longsword/walk/longsword.png",
              "weapon/sword/longsword/universal_behind/walk/longsword.png"),
    "marin": ("weapon/sword/dagger/walk/dagger.png", None),
    "aaron": ("weapon/sword/saber/walk/saber.png",
              "weapon/sword/saber/universal_behind/walk/saber.png"),
}
def wcrop(sheet, i):
    return sheet.crop((i * 64, LEFT_ROW * 64, i * 64 + 64, LEFT_ROW * 64 + 64))
dims = {}
for cid in ["ludo", "marin", "aaron"]:
    fg_rel, bg_rel = WEAPONS[cid]
    fg = Image.open(f"{LPC}/{fg_rel}").convert("RGBA") if fg_rel else None
    bgw = Image.open(f"{LPC}/{bg_rel}").convert("RGBA") if bg_rel else None
    imgs = []
    for i in FRAMES:
        fr = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        if bgw: fr.alpha_composite(wcrop(bgw, i))
        fr.alpha_composite(Image.open(f"{A}/char/{cid}_Left_{i}.png").convert("RGBA"))
        if fg: fr.alpha_composite(wcrop(fg, i))
        imgs.append(fr)
    x1 = min(i.getbbox()[0] for i in imgs); y1 = min(i.getbbox()[1] for i in imgs)
    x2 = max(i.getbbox()[2] for i in imgs); y2 = max(i.getbbox()[3] for i in imgs)
    for n, im in enumerate(imgs):
        c = im.crop((x1, y1, x2, y2))
        c = c.resize((c.width * 4, c.height * 4), Image.NEAREST)
        c.save(f"{A}/battle/hero_{cid}_f{n}.png")
    dims[cid] = [(x2 - x1) * 4, (y2 - y1) * 4]
json.dump(dims, open(f"{A}/battle/hero_dims.json", "w"))

# 指向左的游標箭頭（顯示於目標右側）
cur = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
d = ImageDraw.Draw(cur)
d.polygon([(4, 20), (26, 6), (26, 34)], fill=(255, 224, 96), outline=(120, 84, 20))
d.rectangle([26, 15, 36, 25], fill=(255, 224, 96), outline=(120, 84, 20))
d.line([(8, 20), (24, 11)], fill=(255, 246, 190))
cur.save(f"{A}/ui/cursor.png")
print(json.dumps(dims))
