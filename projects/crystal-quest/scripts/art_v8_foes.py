#!/usr/bin/env python3
"""LPC 人形敵人重製 v8：用 LPC 圖層合成人形怪的正面站立戰鬥圖，取代 16px 商店圖。
輸出單幀到 assets/battle/lpc_src/<sprite>_0.png；build_cq2 的 FOE 迴圈會優先讀這裡（見 LPC_FOES）。
非人形怪（史萊姆/鳥/蟲/飛魔/小魔/魔影/熊）不在此檔——那批走 OGA LPC 生物包（另行處理）。
執行順序：art_v8_foes.py → build_cq2.py → art_v2.py → art_v3_lpc.py"""
import os
from PIL import Image

LPC = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/tools/lpc/spritesheets"
OUT = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/projects/crystal-quest/assets/battle/lpc_src"
os.makedirs(OUT, exist_ok=True)

def tint(img, color):
    if color is None: return img
    r, g, b = color; px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            pr, pg, pb, pa = px[x, y]
            if pa: px[x, y] = (pr*r//255, pg*g//255, pb*b//255, pa)
    return img

def compose(layers):
    base = Image.new("RGBA", (576, 256), (0, 0, 0, 0))
    for rel, color in layers:
        img = Image.open(f"{LPC}/{rel}").convert("RGBA")
        if img.size != (576, 256):                       # 對齊到標準表左上
            tmp = Image.new("RGBA", (576, 256), (0, 0, 0, 0)); tmp.alpha_composite(img); img = tmp
        base.alpha_composite(tint(img, color))
    return base

def front_frame(sheet, scale=1.0):
    fr = sheet.crop((0, 128, 64, 192))                   # Down 列(row2) 第 0 幀＝正面站立
    bb = fr.getbbox()
    if bb: fr = fr.crop(bb)
    if scale != 1.0: fr = fr.resize((max(1,round(fr.width*scale)), max(1,round(fr.height*scale))), Image.NEAREST)
    return fr

MALE = "body/bodies/male/walk.png"
FOES = {
 # 哥布林拾荒者：綠皮、破褲
 "goblin": (1.0, [(MALE,(150,185,110)),("head/heads/goblin/adult/walk.png",None),
                  ("legs/pants/male/walk.png",(96,72,48))]),
 # 獸人挖掘者：灰綠、皮甲、深褲
 "orc": (1.08, [(MALE,(150,168,120)),("head/heads/orc/male/walk.png",None),
                ("legs/pants/male/walk.png",(70,62,52)),("torso/armour/leather/male/walk.png",None)]),
 # 哥布林頭目：深綠壯碩、皮甲（放大＝頭目感）
 "maskedorc": (1.28, [(MALE,(118,150,92)),("head/heads/orc/male/walk.png",None),
                      ("legs/pants/male/walk.png",(58,50,42)),("torso/armour/leather/male/walk.png",None)]),
 # 骷髏礦工：LPC 骷髏身＋骷髏頭（身體無頭需疊頭）＋破褲
 "skeleton": (1.0, [("body/bodies/skeleton/walk/skeleton.png",None),
                    ("head/heads/skeleton/walk/skeleton.png",None),
                    ("legs/pants/male/walk.png",(84,84,94))]),
 # 死靈術士：蒼白人身＋深袍＋兜帽
 "necro": (1.02, [(MALE,(196,196,205)),("head/heads/human/male/walk.png",None),
                  ("legs/skirts/plain/thin/walk.png",(44,42,58)),
                  ("torso/clothes/longsleeve/longsleeve/male/walk.png",(50,48,66)),
                  ("hat/cloth/hood/adult/walk.png",(44,42,58))]),
 # 洞窟食人魔：巨大灰綠、皮甲、腰布（放大最多）
 "ogre": (1.5, [(MALE,(140,158,108)),("head/heads/troll/adult/walk.png",None),
                ("legs/pants/male/walk.png",(92,74,52)),("torso/armour/leather/male/walk.png",None)]),
}

made = []
for sprite, (scale, layers) in FOES.items():
    try:
        fr = front_frame(compose(layers), scale)
        fr.save(f"{OUT}/{sprite}_0.png"); made.append(f"{sprite}({fr.width}x{fr.height})")
    except Exception as e:
        print("!! FAIL", sprite, e)
print("art v8 foes done:", ", ".join(made))
