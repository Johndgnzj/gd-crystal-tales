#!/usr/bin/env python3
"""美術 v14：森林改用 anokolisa Pixel Crawler(Free) 素材。
  - assets/map/atlas_forest.png：森林專屬地面圖集（沿用主 atlas 的 GID 佈局，只換像素）
  - assets/props/fst_tree_*.png：多樹種立體樹（統一 96x120 底部對齊畫布，沿用 TPX/TPY）
  - assets/props/fst_deco_*.png：非阻擋地面裝飾（灌木/蕨/蘑菇/碎石/花）
來源 tools/anokolisa（CC 近似：可商用/改作，不得單獨販售素材，見 LICENSE_Terms.txt；CREDITS 已記）。
在 build_cq2.py 之後執行（產物覆蓋/新增，不動主 atlas.png 與其他地圖）。"""
import os
from PIL import Image, ImageEnhance, ImageDraw

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(_HERE)
GDROOT = os.path.dirname(os.path.dirname(PROJ))
SRC = f"{GDROOT}/tools/anokolisa"
A = f"{PROJ}/assets"
P = f"{A}/props"

FLOORS = Image.open(f"{SRC}/Floors_Tiles.png").convert("RGBA")
VEG = Image.open(f"{SRC}/Vegetation.png").convert("RGBA")
ROCKS = Image.open(f"{SRC}/Rocks.png").convert("RGBA")

def cell16(src, cx, cy): return src.crop((cx * 16, cy * 16, cx * 16 + 16, cy * 16 + 16))
def up2(im): return im.resize((32, 32), Image.NEAREST)

# ===================== 1. 森林地面圖集 =====================
GRASS = cell16(FLOORS, 2, 10)      # 亮綠實心
GRASS_D = cell16(FLOORS, 2, 11)    # 深綠實心
DIRT = cell16(FLOORS, 11, 10)      # 棕土（path/dirt）
CANOPY = Image.open(f"{SRC}/Trees/Model_01/Size_05.png").convert("RGBA").crop((30, 28, 46, 44))

TS, COLS = 32, 6
tiles = ["grass","grassf","path","dirt","tgrass","water","sand","bridge","rockfloor","gravel",
         "cavefloor","cavedark","rail","farm","grass2","grass3","plaza","pn","ps","pw","pe",
         "pnw","pne","psw","pse","pc","pinw","pine","pisw","pise","cwall","cwtop","fwall","ctop"]
G = {n: i + 1 for i, n in enumerate(tiles)}
rows_n = (len(tiles) + COLS - 1) // COLS
atlas = Image.new("RGBA", (COLS * TS, rows_n * TS), (0, 0, 0, 0))
def put(name, im):
    i = G[name] - 1
    atlas.alpha_composite(im if im.size == (TS, TS) else up2(im), ((i % COLS) * TS, (i // COLS) * TS))

put("grass", GRASS)
put("grass2", GRASS_D)
put("grass3", ImageEnhance.Brightness(GRASS).enhance(1.12))
def flowered(base):
    b = up2(base).copy(); d = ImageDraw.Draw(b)
    for x, y, c in [(7, 20, (250, 224, 92)), (20, 9, (248, 250, 236)),
                    (24, 24, (238, 132, 168)), (12, 12, (250, 224, 92))]:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=c + (255,)); d.point((x, y), fill=(90, 70, 30, 255))
    return b
put("grassf", flowered(GRASS))
def tallgrass(base):
    b = up2(base).copy(); d = ImageDraw.Draw(b)
    for bx in (5, 11, 17, 23, 28):
        d.line([(bx, 26), (bx - 2, 15)], fill=(28, 84, 6, 255), width=2)
        d.line([(bx + 3, 27), (bx + 2, 18)], fill=(96, 168, 40, 255), width=1)
    return b
put("tgrass", tallgrass(GRASS))
put("fwall", ImageEnhance.Brightness(up2(CANOPY)).enhance(0.72))
def path_tile(edges, band=12):
    t = up2(DIRT).copy(); g = up2(GRASS)
    mask = Image.new("L", (TS, TS), 0); px = mask.load()
    for y in range(TS):
        for x in range(TS):
            if (("top" in edges and y < band) or ("bottom" in edges and y >= TS - band) or
                ("left" in edges and x < band) or ("right" in edges and x >= TS - band)):
                px[x, y] = 255
    t.paste(g, (0, 0), mask); return t
for nm, e in [("pn", {"top"}), ("ps", {"bottom"}), ("pw", {"left"}), ("pe", {"right"}),
              ("pnw", {"top", "left"}), ("pne", {"top", "right"}),
              ("psw", {"bottom", "left"}), ("pse", {"bottom", "right"})]:
    put(nm, path_tile(e))
put("path", DIRT); put("dirt", DIRT); put("pc", DIRT)
atlas.save(f"{A}/map/atlas_forest.png")
print("saved assets/map/atlas_forest.png", atlas.size)

# atlas_town = 森林地面 superset ＋ 城鎮專用 plaza（夯土廣場）/farm（田）
PLAZA = cell16(FLOORS, 7, 14)                          # 淺沙夯土（城鎮中心）
def farm_tile():                                       # 田＝棕土＋橫向犁溝
    b = up2(DIRT).copy(); d = ImageDraw.Draw(b)
    for yy in range(4, 32, 7):
        d.line([(0, yy), (31, yy)], fill=(96, 66, 40, 200), width=2)
        d.line([(0, yy + 2), (31, yy + 2)], fill=(150, 110, 70, 150), width=1)
    return b
put("plaza", PLAZA); put("farm", farm_tile())
atlas.save(f"{A}/map/atlas_town.png")
print("saved assets/map/atlas_town.png", atlas.size)

# ===================== 2. sprite 自動切割工具 =====================
def _groups(idxs):
    g, s, p = [], None, None
    for i in idxs:
        if s is None: s = i
        elif i != p + 1: g.append((s, p)); s = i
        p = i
    if s is not None: g.append((s, p))
    return g
def sprites(im, min_w=5, min_h=5):
    a = im.split()[3]
    cols = [x for x in range(im.width) if a.crop((x, 0, x + 1, im.height)).getbbox()]
    out = []
    for x0, x1 in _groups(cols):
        strip = im.crop((x0, 0, x1 + 1, im.height)); ar = strip.split()[3]
        rows = [y for y in range(strip.height) if ar.crop((0, y, strip.width, y + 1)).getbbox()]
        for y0, y1 in _groups(rows):
            sub = strip.crop((0, y0, strip.width, y1 + 1)); bb = sub.getbbox()
            if bb:
                sp = sub.crop(bb)
                if sp.width >= min_w and sp.height >= min_h: out.append(sp)
    return out
def _mean(sp):
    op = [p for p in sp.getdata() if p[3] > 128]
    if not op: return (0, 0, 0)
    n = len(op)
    return (sum(p[0] for p in op) / n, sum(p[1] for p in op) / n, sum(p[2] for p in op) / n)
def is_green(sp, k=1.05):
    r, g, b = _mean(sp); return g > r * k and g > b * k
def not_blue(sp, k=1.05):
    r, g, b = _mean(sp); return not (b > r * k and b > g * k)
def has_purple(sp, need=4):   # 含洋紅像素（綠莖紫頂的花也算），排除純綠/棕枝
    c = sum(1 for r, g, b, a in sp.getdata()
            if a > 128 and r > 110 and r > g + 25 and b > g + 10)
    return c >= need

# ===================== 3. 多樹種（統一 96x120 底對齊）=====================
TREE_W, TREE_H = 96, 120                 # 與 build_cq2 的 TREE_W/H 一致 → 沿用 TPX/TPY
raw_trees = []
for m, s in [("Model_01", "Size_04"), ("Model_02", "Size_04"), ("Model_03", "Size_04"),
             ("Model_02", "Size_03"), ("Model_03", "Size_03"), ("Model_01", "Size_03")]:
    sh = Image.open(f"{SRC}/Trees/{m}/{s}.png").convert("RGBA")
    for sp in sprites(sh, min_w=24, min_h=40):
        if is_green(sp) and sp.height >= 48:
            raw_trees.append(sp)
# 依高度分散挑 6 棵（去重相近）
raw_trees.sort(key=lambda s: s.width * s.height)
pick = []
if raw_trees:
    idxs = [round(i * (len(raw_trees) - 1) / 5) for i in range(6)]
    pick = [raw_trees[i] for i in sorted(set(idxs))]
# 目標視覺高度（製造大小變化），全部底對齊在 96x120
target_h = [116, 110, 100, 96, 86, 78]
for i, sp in enumerate(pick):
    th = target_h[i % len(target_h)]
    sc = min(TREE_W / sp.width, th / sp.height)
    r = sp.resize((max(1, round(sp.width * sc)), max(1, round(sp.height * sc))), Image.LANCZOS)
    canvas = Image.new("RGBA", (TREE_W, TREE_H), (0, 0, 0, 0))
    canvas.alpha_composite(r, ((TREE_W - r.width) // 2, TREE_H - r.height))
    canvas.save(f"{P}/fst_tree_{i+1}.png")
NTREE = len(pick)
print(f"saved {NTREE} x fst_tree_*.png (96x120)")

# ===================== 4. 非阻擋地面裝飾 =====================
def save_scaled(sp, name, maxdim):
    sc = min(maxdim / sp.width, maxdim / sp.height, 1.0)
    if sc < 1.0:
        sp = sp.resize((max(1, round(sp.width * sc)), max(1, round(sp.height * sc))), Image.LANCZOS)
    sp.save(f"{P}/{name}.png")

veg_sp = sprites(VEG, min_w=8, min_h=8)
bushes = sorted([sp for sp in veg_sp if is_green(sp) and 20 <= sp.width <= 64 and 20 <= sp.height <= 64],
                key=lambda s: -s.width * s.height)
if bushes: save_scaled(bushes[0], "fst_deco_bush", 30)
# 蕨/小草叢：綠、細高；缺就用灌木縮小
ferns = [sp for sp in veg_sp if is_green(sp) and sp.width <= 20 and 10 <= sp.height <= 28]
if ferns: save_scaled(sorted(ferns, key=lambda s: -s.height)[0], "fst_deco_fern", 22)
elif bushes: save_scaled(bushes[0], "fst_deco_fern", 18)
# 蘑菇（Vegetation 底部區）
mush = [sp for sp in sprites(VEG.crop((16, 316, 120, 356))) if not_blue(sp) and 6 <= sp.width <= 22]
if mush: save_scaled(sorted(mush, key=lambda s: -s.width * s.height)[0], "fst_deco_mush", 16)
# 紫花叢（限洋紅色，排除鄰近棕枝）
flow = [sp for sp in sprites(VEG.crop((180, 158, 240, 212))) if has_purple(sp) and sp.height >= 8]
if flow: save_scaled(sorted(flow, key=lambda s: -s.height)[0], "fst_deco_flower", 18)
else: print("WARN: 未找到紫花，fst_deco_flower 未更新")
# 碎石（Rocks 最小者）
rk = sorted(sprites(ROCKS, min_w=6, min_h=5), key=lambda s: s.width * s.height)
if rk: save_scaled(rk[0], "fst_deco_pebble", 14)

made = sorted(f for f in os.listdir(P) if f.startswith("fst_deco_"))
print("saved decor:", made)
