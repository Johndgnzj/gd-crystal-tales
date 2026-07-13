#!/usr/bin/env python3
"""美術精細化 v2：同尺寸重繪 atlas 與道具（在 build_cq2.py 之後執行覆蓋）"""
import random
from PIL import Image, ImageDraw

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ  = os.path.dirname(_HERE)
GDROOT = os.path.dirname(os.path.dirname(PROJ))
A = f"{PROJ}/assets"
random.seed(99)
TS = 32
tiles = ["grass","grassf","path","dirt","tgrass","water","sand","bridge",
         "rockfloor","gravel","cavefloor","cavedark","rail","farm",
         "grass2","grass3","plaza",
         "pn","ps","pw","pe","pnw","pne","psw","pse","pc",
         "pinw","pine","pisw","pise"]
COLS = 6
rows_n = (len(tiles)+COLS-1)//COLS
atlas = Image.open(f"{A}/map/atlas.png").convert("RGBA")   # 以 LPC 版為底，只補非 LPC 磚
d = ImageDraw.Draw(atlas)
def cell(i): return ((i%COLS)*TS,(i//COLS)*TS)

def dither(i, base, tones, density=0.55, blob=2):
    """基底色+多色抖動叢，讓圖磚有機不死板"""
    x,y = cell(i)
    d.rectangle([x,y,x+TS-1,y+TS-1],fill=base)
    n = int(TS*TS*density/ (blob*blob))
    for _ in range(n):
        sx,sy = x+random.randint(0,TS-blob), y+random.randint(0,TS-blob)
        c = random.choice(tones)
        d.rectangle([sx,sy,sx+blob-1,sy+blob-1],fill=c)

def wrap_dither(i, base, tones, density=0.55, blob=2):
    """toroidal 抖動：blob 跨格右/下邊會 wrap 到對邊 → 單格 32px 可無縫平鋪(左右/上下接得起來)"""
    x,y = cell(i)
    d.rectangle([x,y,x+TS-1,y+TS-1],fill=base)
    n = int(TS*TS*density/(blob*blob))
    for _ in range(n):
        sx,sy = random.randint(0,TS-1), random.randint(0,TS-1)
        c = random.choice(tones)
        for ox in range(blob):
            for oy in range(blob):
                d.point((x+(sx+ox)%TS, y+(sy+oy)%TS), fill=c)

def icrack(i, col, n=2):
    """格內裂縫：端點限制在內側(不觸格邊)→ 不破壞平鋪連續性"""
    x,y = cell(i)
    for _ in range(n):
        cx,cy = x+random.randint(4,TS-10), y+random.randint(4,TS-8)
        d.line([(cx,cy),(cx+random.randint(3,5),cy+random.randint(1,4))],fill=col)

# 5 水：深淺帶+波光
dither(5,(58,118,205),[(52,108,192),(66,130,218),(48,100,182)],0.4)
x,y=cell(5)
for wy in (7,17,26):
    wx=x+random.randint(2,10)
    d.arc([wx,y+wy-2,wx+11,y+wy+3],200,340,fill=(130,185,245))
# 6 沙
dither(6,(226,206,146),[(216,196,136),(236,216,156),(208,188,130)])
# 7 橋（木板+釘）
x,y=cell(7)
d.rectangle([x,y,x+TS-1,y+TS-1],fill=(156,114,72))
for by in range(0,TS,8):
    d.line([(x,y+by),(x+TS-1,y+by)],fill=(118,84,52))
    d.line([(x,y+by+1),(x+TS-1,y+by+1)],fill=(172,130,86))
    d.point((x+3,y+by+4),fill=(90,64,40)); d.point((x+TS-4,y+by+4),fill=(90,64,40))
d.line([(x,y),(x,y+TS-1)],fill=(110,78,48)); d.line([(x+TS-1,y),(x+TS-1,y+TS-1)],fill=(110,78,48))
# === 地下岩石家族（無縫平鋪；礦坑暖中性灰 → 洞穴冷暗灰＝更深地底，讀起來連續）===
# 8 礦區岩地：暖中性灰岩
wrap_dither(8,(150,144,136),[(140,134,126),(160,154,146),(132,126,118),(147,150,143)],0.5)
icrack(8,(116,110,102))
# 9 碎石（遇敵）：同岩石、較亮較粗糙以便辨識遇敵區，但對比降低避免格狀＋無縫
wrap_dither(9,(151,143,131),[(133,125,113),(167,159,147),(122,116,106),(159,153,141)],0.62)
# 10 洞穴地：同岩石家族、冷灰偏暗（更深）
wrap_dither(10,(92,90,100),[(84,82,92),(102,100,110),(78,76,86),(96,96,106)],0.5)
icrack(10,(66,64,74))
# 11 洞穴暗部：最深
wrap_dither(11,(56,54,66),[(50,48,60),(64,62,74),(52,52,62)],0.42)
# 8/10 主地板改用 OGA LPC cobblestone（[LPC] Dungeon Elements, Sharm, CC-BY）：
#   去飽和→套礦坑/洞穴灰階（保留鋪石細節、仍無縫）；gravel(9,遇敵)/cavedark(11) 維持自繪以資區別
_COB=Image.open(f"{GDROOT}/tools/lpc-dungeon/cobble.png").convert("RGBA")
def _lumtint(src,tint):
    out=Image.new("RGBA",(TS,TS),(0,0,0,0)); sp=src.load(); op=out.load()
    for yy in range(TS):
        for xx in range(TS):
            r,g,b,a=sp[xx,yy]; L=(r*30+g*59+b*11)//100
            op[xx,yy]=(min(255,L*tint[0]//150),min(255,L*tint[1]//150),min(255,L*tint[2]//150),a)
    return out
atlas.paste(_lumtint(_COB,(156,150,142)),cell(8))   # rockfloor 礦坑：暖中性灰鋪石
atlas.paste(_lumtint(_COB,(92,90,102)), cell(10))    # cavefloor 洞穴：冷暗灰鋪石
# 12 軌道
x,y=cell(12)
d.rectangle([x,y,x+TS-1,y+TS-1],fill=(146,138,130))
for _ in range(14):
    sx,sy=x+random.randint(0,TS-2),y+random.randint(0,TS-2)
    d.rectangle([sx,sy,sx+1,sy+1],fill=random.choice([(136,128,120),(156,148,140)]))
for by in range(2,TS,7): d.rectangle([x+4,y+by,x+27,y+by+2],fill=(112,86,54),outline=(94,70,44))
d.rectangle([x+7,y,x+9,y+TS-1],fill=(105,100,95)); d.line([(x+7,y),(x+7,y+TS-1)],fill=(140,135,130))
d.rectangle([x+22,y,x+24,y+TS-1],fill=(105,100,95)); d.line([(x+22,y),(x+22,y+TS-1)],fill=(140,135,130))
# 13 農田：壟溝+作物點
x,y=cell(13)
d.rectangle([x,y,x+TS-1,y+TS-1],fill=(138,98,60))
for by in range(2,TS,8):
    d.line([(x,y+by),(x+TS-1,y+by)],fill=(112,78,46),width=2)
    d.line([(x,y+by+2),(x+TS-1,y+by+2)],fill=(156,112,70))
for _ in range(4):
    px_,py_=x+random.randint(2,TS-4),y+random.randint(4,TS-4)
    d.ellipse([px_,py_,px_+2,py_+2],fill=(96,160,66))
atlas.save(f"{A}/map/atlas.png")

# ============ 道具重繪（同尺寸）============
P=f"{A}/props"
def save(img,n): img.save(f"{P}/{n}")

# 灌木 36x26
img=Image.new("RGBA",(36,26),(0,0,0,0)); dd=ImageDraw.Draw(img)
dd.ellipse([2,20,34,25],fill=(30,60,30,80))
for cx,cy,r,c in [(18,14,12,(44,110,48)),(10,16,8,(52,124,54)),(26,16,8,(52,124,54)),(18,10,8,(64,142,62))]:
    dd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
for _ in range(8): dd.point((random.randint(6,30),random.randint(4,20)),fill=(90,168,84))
save(img,"bush.png")

# 石頭 36x26
img=Image.new("RGBA",(36,26),(0,0,0,0)); dd=ImageDraw.Draw(img)
dd.ellipse([3,20,33,25],fill=(40,40,46,80))
dd.polygon([(4,20),(9,8),(20,4),(30,10),(33,20),(26,24),(9,24)],fill=(142,140,148),outline=(96,94,104))
dd.polygon([(9,8),(20,4),(24,9),(13,13)],fill=(168,166,176))
dd.line([(13,13),(11,21)],fill=(112,110,120)); dd.line([(20,11),(24,20)],fill=(112,110,120))
save(img,"rock.png")

# 房屋（重繪：木骨架+屋瓦+煙囪+門拱+窗台）
def make_house(wall,roof,banner=None,W=160,H=140):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); dd=ImageDraw.Draw(img)
    dd.ellipse([6,H-10,W-6,H-2],fill=(30,50,30,70))
    dd.rectangle([10,50,W-10,H-4],fill=wall,outline=(72,52,36),width=2)          # 牆
    dk=tuple(max(0,v-26) for v in wall)
    for bx in (10,W//2-2,W-14): dd.rectangle([bx,50,bx+4,H-4],fill=dk)           # 木骨架直樑
    dd.rectangle([10,88,W-10,92],fill=dk)                                        # 橫樑
    dd.rectangle([10,50,W-10,56],fill=(60,44,32,90))                             # 屋簷陰影
    rdk=tuple(max(0,v-30) for v in roof); rlt=tuple(min(255,v+22) for v in roof)
    dd.polygon([(0,52),(W//2,4),(W,52)],fill=roof,outline=(58,36,26))            # 屋頂
    for t in range(1,5):                                                          # 瓦片層
        yy=8+t*9
        x1=int((W//2)*(yy-4)/48*0.96); dd.line([(W//2-x1,yy+4),(W//2+x1,yy+4)],fill=rdk,width=2)
        dd.line([(W//2-x1,yy+2),(W//2+x1,yy+2)],fill=rlt)
    dd.rectangle([W-46,10,W-32,34],fill=(120,96,84),outline=(78,60,48))          # 煙囪
    dd.rectangle([W-48,8,W-30,14],fill=(96,76,64),outline=(70,54,42))
    # 門（拱形+板+鉚釘）
    dcx=W//2
    dd.rectangle([dcx-14,H-46,dcx+14,H-4],fill=(112,78,48),outline=(64,44,28),width=2)
    dd.pieslice([dcx-14,H-58,dcx+14,H-34],180,360,fill=(112,78,48),outline=(64,44,28))
    for py in range(H-42,H-6,8): dd.line([(dcx-11,py),(dcx+11,py)],fill=(92,62,38))
    dd.ellipse([dcx+6,H-28,dcx+10,H-24],fill=(235,205,95),outline=(150,120,50))
    # 窗（窗台+十字框+微光）
    for wx in (24,W-54):
        dd.rectangle([wx-2,94,wx+32,98],fill=dk)                                 # 窗台
        dd.rectangle([wx,66,wx+30,94],fill=(150,200,232),outline=(72,52,36),width=2)
        dd.polygon([(wx+2,68),(wx+12,68),(wx+2,80)],fill=(210,235,250))
        dd.line([(wx+15,66),(wx+15,94)],fill=(72,52,36),width=2)
        dd.line([(wx,80),(wx+30,80)],fill=(72,52,36),width=2)
    if banner:
        dd.rectangle([dcx-11,16,dcx+11,48],fill=banner,outline=(46,38,30),width=2)
        dd.polygon([(dcx-11,48),(dcx,40),(dcx+11,48)],fill=roof)
        dd.ellipse([dcx-5,24,dcx+5,34],outline=(240,230,180))
    return img
save(make_house((224,200,160),(96,116,158),banner=(58,108,196)),"b_guild.png")
save(make_house((230,206,166),(182,88,66)),"b_inn.png")
save(make_house((208,208,214),(122,90,68)),"b_mayor.png")
save(make_house((216,198,172),(98,142,92)),"b_shop.png")
save(make_house((192,182,178),(82,80,88)),"b_smith.png")

# 小神殿 120x130
img=Image.new("RGBA",(120,130),(0,0,0,0)); dd=ImageDraw.Draw(img)
dd.ellipse([6,122,114,129],fill=(30,50,30,70))
dd.rectangle([12,52,108,126],fill=(240,236,228),outline=(118,108,98),width=2)
for bx in (12,56,104): dd.rectangle([bx,52,bx+3,126],fill=(214,208,198))
dd.polygon([(2,54),(60,6),(118,54)],fill=(204,194,178),outline=(108,98,88))
for t in range(1,4):
    yy=10+t*11; x1=int(58*(yy-6)/48*0.95)
    dd.line([(60-x1,yy+4),(60+x1,yy+4)],fill=(180,170,155),width=2)
dd.ellipse([48,16,72,40],fill=(244,226,150),outline=(150,128,74),width=2)        # 女神徽記
dd.ellipse([54,22,66,34],fill=(150,192,122),outline=(96,140,80))
dd.pieslice([46,84,74,112],180,360,fill=(158,128,96),outline=(94,74,54))         # 拱門
dd.rectangle([46,98,74,126],fill=(158,128,96),outline=(94,74,54))
dd.rectangle([50,100,70,126],fill=(66,52,40))
save(img,"b_shrine.png")

# 水井 64x76（石造，配合石系建築；新版）
img=Image.new("RGBA",(64,76),(0,0,0,0)); dd=ImageDraw.Draw(img)
dd.ellipse([8,70,56,75],fill=(20,28,18,90))                                  # 地面陰影
# 石造井身＋石塊縫
dd.rectangle([11,50,53,70],fill=(150,150,158),outline=(88,88,100),width=1)
dd.ellipse([11,62,53,76],fill=(150,150,158),outline=(88,88,100),width=2)     # 底弧
for _sx in (22,32,42): dd.line([(_sx,51),(_sx,69)],fill=(120,120,132))       # 直縫
for _sy in (57,64):    dd.line([(12,_sy),(52,_sy)],fill=(120,120,132))       # 橫縫
dd.ellipse([11,44,53,58],fill=(126,126,136),outline=(88,88,100),width=2)     # 井口環
dd.ellipse([16,46,48,56],fill=(40,54,78))                                    # 水面
dd.arc([20,48,44,55],200,340,fill=(120,150,190))                             # 水光
# 木柱＋斜頂
dd.rectangle([12,14,16,48],fill=(120,88,54),outline=(80,58,34))
dd.rectangle([48,14,52,48],fill=(120,88,54),outline=(80,58,34))
dd.polygon([(4,18),(32,3),(60,18)],fill=(150,98,60),outline=(84,56,32))      # 屋頂
for _t in range(1,4):
    _yy=6+_t*4; _x1=int(28*(_yy-2)/16)
    dd.line([(32-_x1,_yy+2),(32+_x1,_yy+2)],fill=(120,78,46))
dd.line([(13,16),(51,16)],fill=(92,66,40),width=2)                           # 橫樑
dd.line([(32,17),(32,44)],fill=(74,62,52))                                   # 繩
dd.rectangle([28,42,36,50],fill=(128,96,58),outline=(84,58,34))              # 木桶
dd.line([(29,44),(35,44)],fill=(152,116,72))
save(img,"well.png")
print("art v2 done")
