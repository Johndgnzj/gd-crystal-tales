#!/usr/bin/env python3
"""美術 v3：用 LPC Tile Atlas(1/2) 手繪建築取代程式畫房屋；洞窟磚/石筍/礦坑口。
   在 build_cq2.py 與 art_v2.py 之後執行覆蓋。素材授權 CC-BY-SA 3.0 / GPL 3.0（見 CREDITS）。"""
from PIL import Image, ImageDraw

T = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/tools"
A = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/projects/crystal-quest/assets"
B = Image.open(f"{T}/lpc-atlas2/build_atlas.png").convert("RGBA")   # 建築組件
O = Image.open(f"{T}/lpc-atlas1/base_out_atlas.png").convert("RGBA") # 戶外/洞窟

def crop(src, x1, y1, x2, y2): return src.crop((x1, y1, x2, y2))
def trim(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im
def canvas(w, h): return Image.new("RGBA", (w, h), (0, 0, 0, 0))
def save(im, name): im.save(f"{A}/props/{name}.png")
def tile_fill(dst, tile, x1, y1, x2, y2):
    for yy in range(y1, y2, tile.height):
        for xx in range(x1, x2, tile.width):
            dst.alpha_composite(tile.crop((0, 0, min(tile.width, x2 - xx), min(tile.height, y2 - yy))), (xx, yy))

SLATE = crop(B, 928, 832, 960, 864)          # 深石板瓦 fill
BRICKBAND = crop(O, 0, 354, 84, 382)         # 紅磚+石簷帶
TUDOR = crop(B, 96, 384, 224, 512)           # 都鐸框板暗磚牆 128x128
DOOR_BROWN = trim(crop(O, 160, 288, 192, 352)).resize((40, 56), Image.NEAREST)
SIGN_SWORD = crop(B, 608, 640, 640, 672)
SIGN_MONEY = crop(B, 640, 640, 672, 672)
SIGN_INN = crop(B, 672, 640, 704, 672)

# ---------- 1. 公會（維多利亞雙層樓 + 錢袋招牌） ----------
g = canvas(160, 258)
g.alpha_composite(crop(B, 236, 764, 396, 1022), (0, 0))          # 雙層門面
g.alpha_composite(crop(B, 128, 896, 224, 1022), (32, 132))       # 哥德式橙門(含框)
g.alpha_composite(SIGN_MONEY, (10, 160))
save(g, "b_guild")

# ---------- 2. 旅店（都鐸暗磚 + 紅磚簷帶 + INN 招牌） ----------
inn = canvas(160, 156)
inn.alpha_composite(TUDOR, (0, 28))
inn.alpha_composite(TUDOR.crop((0, 0, 32, 128)), (128, 28))
tile_fill(inn, BRICKBAND, 0, 0, 160, 28)
inn.alpha_composite(DOOR_BROWN, (60, 100))
inn.alpha_composite(SIGN_INN, (16, 88))
save(inn, "b_inn")

# ---------- 3. 鎮長宅（淺石大宅 + 拱形雙窗 + 紅大門） ----------
m = canvas(160, 168)
stone = crop(B, 64, 816, 128, 880)                               # 淺石牆 fill 64x64
tile_fill(m, stone, 0, 20, 160, 168)
m.alpha_composite(crop(B, 0, 768, 128, 788), (0, 0))             # 齒飾簷口
m.alpha_composite(crop(B, 0, 768, 128, 788).crop((0, 0, 32, 20)), (128, 0))
m.alpha_composite(crop(B, 768, 768, 864, 856), (12, 30))         # 拱形雙窗
door_r = trim(crop(B, 770, 894, 832, 982))                        # 紅大門
m.alpha_composite(door_r, (104, 168 - door_r.height))
save(m, "b_mayor")

# ---------- 4. 道具店（維多利亞單層 + 大陳列窗 + 紅簾門） ----------
s = canvas(160, 150)
s.alpha_composite(crop(B, 224, 880, 384, 1022), (0, 8))          # 一樓門面(雙暗窗)
s.alpha_composite(crop(B, 378, 906, 472, 1022), (62, 34))        # 奶油色大陳列窗
s.alpha_composite(crop(B, 128, 772, 182, 878), (8, 44))          # 紅簾入口
s.alpha_composite(SIGN_MONEY, (10, 52))
save(s, "b_shop")

# ---------- 5. 鐵匠鋪（都鐸暗磚 + 石板瓦 + 黑爐 + 劍招牌） ----------
sm = canvas(160, 156)
sm.alpha_composite(TUDOR, (0, 28))
sm.alpha_composite(TUDOR.crop((0, 0, 32, 128)), (128, 28))
tile_fill(sm, SLATE, 0, 0, 160, 28)
stove = trim(crop(O, 640, 448, 672, 512))                         # 黑鑄爐
sm.alpha_composite(stove, (120, 156 - stove.height))
sm.alpha_composite(DOOR_BROWN, (48, 100))
sm.alpha_composite(SIGN_SWORD, (14, 88))
save(sm, "b_smith")

# ---------- 6. 小神殿（白石塊 + 白拱門 + 火炬 + 女神徽） ----------
sh = canvas(128, 170)
wall = crop(B, 768, 576, 864, 632)                                # 白石大塊牆帶 96x56（避開帶洞磚列）
tile_fill(sh, wall, 0, 42, 128, 170)
arch = trim(crop(O, 228, 370, 284, 416))                          # 白石拱門
arch = arch.resize((arch.width * 2, arch.height * 2), Image.NEAREST)
sh.alpha_composite(arch, (64 - arch.width // 2, 170 - arch.height))
tor = trim(crop(B, 992, 704, 1024, 768))                          # 立火炬
sh.alpha_composite(tor, (8, 170 - tor.height))
sh.alpha_composite(tor, (128 - 8 - tor.width, 170 - tor.height))
dd = ImageDraw.Draw(sh)
dd.ellipse([48, 8, 80, 40], fill=(244, 226, 150), outline=(150, 128, 74), width=2)  # 女神徽記
dd.ellipse([56, 16, 72, 32], fill=(150, 192, 122), outline=(96, 140, 80))
save(sh, "b_shrine")

# ---------- 7. 礦坑口（岩紋理山體；prop 放 tile19、洞口對齊 tile21-22 ＝局部 x64..128） ----------
cm = canvas(160, 112)
rockt = crop(O, 544, 96, 576, 128)                                # 沙色圓石紋理 fill
body = Image.new("RGBA", (160, 112), (196, 158, 102, 255))        # 沙色底（補紋理磚的透明點）
tile_fill(body, rockt, 0, 0, 160, 112)
mmask = Image.new("L", (160, 112), 0)
mdd = ImageDraw.Draw(mmask)
mdd.polygon([(0, 112), (10, 44), (44, 10), (116, 10), (150, 44), (160, 112)], fill=255)
cm.paste(body, (0, 0), mmask)
cdd = ImageDraw.Draw(cm)
cdd.line([(0, 112), (10, 44), (44, 10), (116, 10), (150, 44), (160, 112)], fill=(70, 52, 40), width=2)
cdd.ellipse([58, 34, 134, 150], fill=(22, 19, 24))                # 洞口（68 寬，罩住 2 格通道）
cdd.rectangle([64, 60, 128, 112], fill=(22, 19, 24))
cdd.rectangle([52, 32, 60, 112], fill=(110, 84, 54))              # 木柱框
cdd.rectangle([132, 32, 140, 112], fill=(110, 84, 54))
cdd.rectangle([48, 24, 144, 36], fill=(126, 98, 62), outline=(80, 60, 40))  # 門楣
save(cm, "cavemouth")

# ---------- 8. 石筍（洞窟裝飾；三組各約 32px 寬，y254-287 避開下方櫃檯） ----------
save(trim(crop(O, 0, 254, 33, 287)), "stal_gold")
save(trim(crop(O, 33, 254, 63, 287)), "stal_brown")
save(trim(crop(O, 63, 254, 97, 287)), "stal_black")

# ---------- 9. LPC 灌木（取代手繪 bush） ----------
save(trim(crop(O, 768, 384, 832, 448)), "bush")

# ---------- 10. 選單地圖頁：區域地圖縮圖 ----------
P2 = "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop/projects/crystal-quest/design/芳蕾鎮區域地圖.png"
rm = Image.open(P2).convert("RGBA")
rm.thumbnail((640, 360), Image.LANCZOS)
rm.save(f"{A}/ui/region_map.png")

print("art v3 (LPC buildings) done")
