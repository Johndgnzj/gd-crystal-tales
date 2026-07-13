#!/usr/bin/env python3
"""室內家具 v12：程序繪製前向 2.5D 家具與房間外殼（floor+牆），供物件擺放式室內用。
   風格對齊既有程序 props（chest/barrel/well）——暖木＋石＋鐵＋布，1px 深色描邊。
   輸出到 assets/props/：int_room_wood.png / int_room_stone.png ＋ f_*.png。須在 build_cq2.py 之前跑。"""
from PIL import Image, ImageDraw

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ  = os.path.dirname(_HERE)
A = f"{PROJ}/assets/props"

# ---- 調色盤 ----
WOOD   =(150,112,72); WOOD_D =(116,84,52); WOOD_L =(178,138,96); WOOD_XD=(84,60,38)
STONE  =(150,150,158);STONE_D=(112,112,122);STONE_L=(178,178,186)
IRON   =(74,78,88);   IRON_L =(126,132,146);IRON_D =(44,46,54)
CLOTH_R=(158,64,60);  CLOTH_B=(70,88,150);  CLOTH_G=(78,124,82); CLOTH_W=(214,208,196)
GOLD   =(214,176,86); FIRE1=(250,196,86); FIRE2=(232,120,44); GLASS=(150,200,214)
OUT    =(38,30,28,255)

def img(w,h): return Image.new("RGBA",(w,h),(0,0,0,0))
def outline(im):
    px=im.load(); w,h=im.size; edge=[]
    for y in range(h):
        for x in range(w):
            if px[x,y][3]>20: continue
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx,ny=x+dx,y+dy
                if 0<=nx<w and 0<=ny<h and px[nx,ny][3]>20: edge.append((x,y)); break
    for x,y in edge: px[x,y]=OUT
    return im
def save(im,name): outline(im).save(f"{A}/{name}.png")

# ---------- 房間外殼 ----------
RW,RH,WALL,SIDE = 720,520,84,18   # 房間圖尺寸、上牆高、側牆寬
def plank_floor(d,x0,y0,x1,y1,base,dk,lt):
    d.rectangle([x0,y0,x1,y1],fill=base)
    ph=26
    for i,yy in enumerate(range(y0,y1,ph)):
        d.line([x0,yy,x1,yy],fill=dk)                       # 板縫
        off=(i%2)*90
        for xx in range(x0+off,x1,180): d.line([xx,yy,xx,min(yy+ph,y1)],fill=dk)
        d.line([x0,yy+2,x1,yy+2],fill=lt)                   # 高光
def flag_floor(d,x0,y0,x1,y1):
    d.rectangle([x0,y0,x1,y1],fill=STONE_D)
    import hashlib
    bw,bh=46,34
    for r,yy in enumerate(range(y0,y1,bh)):
        off=(r%2)*23
        for xx in range(x0-off,x1,bw):
            x2,y2=min(xx+bw-3,x1),min(yy+bh-3,y1)
            if x2>xx+4 and y2>yy+4:
                d.rectangle([max(xx,x0),yy,x2,y2],fill=STONE)
                d.line([max(xx,x0),yy,x2,yy],fill=STONE_L)
def room(kind):
    im=img(RW,RH); d=ImageDraw.Draw(im)
    if kind=="wood":
        plank_floor(d,0,WALL,RW,RH,WOOD,WOOD_D,WOOD_L)
        d.rectangle([0,0,RW,WALL],fill=(120,92,64)); d.rectangle([0,WALL-6,RW,WALL],fill=WOOD_XD)
        for xx in range(0,RW,24): d.line([xx,0,xx,WALL-6],fill=(104,78,52))   # 牆板
        wl=(96,72,50)
    else:
        flag_floor(d,0,WALL,RW,RH)
        d.rectangle([0,0,RW,WALL],fill=(120,120,130)); d.rectangle([0,WALL-6,RW,WALL],fill=(90,90,100))
        for r in range(0,WALL-6,20):
            off=((r//20)%2)*24
            for xx in range(-off,RW,48): d.rectangle([xx,r,xx+46,r+18],outline=(96,96,106))
        wl=(150,150,160)
    # 側牆陰影＋地板內緣暗角
    d.rectangle([0,WALL,SIDE,RH],fill=(0,0,0,60)); d.rectangle([RW-SIDE,WALL,RW,RH],fill=(0,0,0,60))
    d.rectangle([0,RH-10,RW,RH],fill=(0,0,0,70))
    # 兩扇窗
    for wx in (150,RW-150-70):
        d.rectangle([wx,20,wx+70,58],fill=(58,64,74)); d.rectangle([wx+3,23,wx+67,55],fill=GLASS)
        d.line([wx+35,23,wx+35,55],fill=(58,64,74)); d.line([wx+3,39,wx+67,39],fill=(58,64,74))
    # 底部中央門口（出口）：門框＋踏墊
    dx0,dx1=RW//2-64,RW//2+64
    d.rectangle([dx0,RH-14,dx1,RH-1],fill=(120,90,60)); d.rectangle([dx0+10,RH-11,dx1-10,RH-3],fill=(150,120,80))
    im.save(f"{A}/int_room_{kind}.png")   # 房間外殼不加 outline
room("wood"); room("stone")

# ---------- 家具 ----------
def bed():
    im=img(48,64); d=ImageDraw.Draw(im)
    d.rectangle([2,4,45,60],fill=WOOD_D)                    # 床架
    d.rectangle([4,2,44,14],fill=WOOD_L)                    # 床頭板
    d.rectangle([5,15,43,58],fill=CLOTH_B)                  # 被
    d.rectangle([5,15,43,26],fill=CLOTH_W)                  # 枕
    d.rectangle([5,40,43,42],fill=(58,72,124))              # 摺線
    save(im,"f_bed")
def table():
    im=img(64,48); d=ImageDraw.Draw(im)
    d.rectangle([6,40,12,47],fill=WOOD_XD); d.rectangle([52,40,58,47],fill=WOOD_XD)   # 桌腳
    d.ellipse([2,6,62,40],fill=WOOD); d.ellipse([2,6,62,34],fill=WOOD_L)              # 桌面
    d.ellipse([2,6,62,40],outline=WOOD_D)
    save(im,"f_table")
def chair():
    im=img(28,34); d=ImageDraw.Draw(im)
    d.rectangle([5,2,23,18],fill=WOOD_L); d.rectangle([7,4,21,16],fill=WOOD)          # 椅背
    d.rectangle([4,18,24,28],fill=WOOD); d.rectangle([5,28,8,33],fill=WOOD_XD); d.rectangle([20,28,23,33],fill=WOOD_XD)
    save(im,"f_chair")
def stool():
    im=img(26,26); d=ImageDraw.Draw(im)
    d.ellipse([2,6,24,22],fill=WOOD); d.ellipse([2,4,24,18],fill=WOOD_L)
    d.rectangle([5,20,8,25],fill=WOOD_XD); d.rectangle([18,20,21,25],fill=WOOD_XD)
    save(im,"f_stool")
def counter():
    im=img(140,46); d=ImageDraw.Draw(im)
    d.rectangle([2,14,137,44],fill=WOOD_D)                  # 櫃身
    for xx in range(2,138,26): d.line([xx,14,xx,44],fill=WOOD_XD)
    d.rectangle([0,6,139,16],fill=WOOD_L); d.rectangle([0,14,139,17],fill=WOOD)      # 檯面
    save(im,"f_counter")
def shelf():
    im=img(58,66); d=ImageDraw.Draw(im)
    d.rectangle([2,2,55,64],fill=WOOD_D)
    for yy in (10,28,46): d.rectangle([5,yy,52,yy+3],fill=WOOD_XD)                    # 層板
    d.rectangle([4,2,53,4],fill=WOOD_L)
    for bx in range(8,50,9):                                                          # 書/罐
        import random; random.seed(bx); c=random.choice([CLOTH_R,CLOTH_B,CLOTH_G,GOLD])
        d.rectangle([bx,12,bx+6,25],fill=c); d.rectangle([bx,30,bx+6,43],fill=random.choice([CLOTH_G,CLOTH_R]))
    save(im,"f_shelf")
def goods():   # 道具店貨架（藥水瓶罐）
    im=img(58,66); d=ImageDraw.Draw(im)
    d.rectangle([2,2,55,64],fill=WOOD_D)
    for yy in (14,34,54): d.rectangle([4,yy,53,yy+2],fill=WOOD_XD)
    pots=[(CLOTH_R,), (CLOTH_B,),(CLOTH_G,),(GOLD,)]
    import random
    for i,yy in enumerate((4,24,44)):
        for j,bx in enumerate(range(8,52,12)):
            c=pots[(i+j)%4][0]
            d.ellipse([bx,yy+4,bx+8,yy+13],fill=c); d.rectangle([bx+3,yy,bx+5,yy+5],fill=(210,210,200))
    save(im,"f_goods")
def rug():   # 地毯（無碰撞）
    im=img(120,80); d=ImageDraw.Draw(im)
    d.rectangle([0,0,119,79],fill=CLOTH_R); d.rectangle([6,6,113,73],outline=GOLD,width=3)
    d.rectangle([16,16,103,63],fill=(128,50,48)); d.rectangle([16,16,103,63],outline=GOLD)
    im.save(f"{A}/f_rug.png")   # 地毯不加外框描邊
def hearth(forge=False):
    im=img(72,58); d=ImageDraw.Draw(im)
    d.rectangle([2,6,69,56],fill=STONE_D); d.rectangle([4,8,67,54],fill=STONE)        # 石壁爐
    for xx in range(4,68,16): d.line([xx,8,xx,54],fill=STONE_D)
    d.rectangle([16,24,55,54],fill=(20,16,18))                                        # 爐膛
    d.polygon([(24,52),(36,28),(48,52)],fill=FIRE2); d.polygon([(30,52),(36,36),(42,52)],fill=FIRE1)
    if forge:
        d.rectangle([2,2,69,10],fill=IRON); d.rectangle([50,2,60,54],fill=IRON_D)     # 煙囪/風箱
    save(im,"f_forge" if forge else "f_hearth")
def altar():
    im=img(72,54); d=ImageDraw.Draw(im)
    d.rectangle([6,20,65,52],fill=STONE); d.rectangle([6,20,65,24],fill=STONE_L)      # 石台
    d.rectangle([2,26,69,40],fill=CLOTH_W); d.rectangle([2,26,69,29],fill=(190,184,170))
    d.polygon([(36,2),(30,20),(42,20)],fill=GOLD)                                     # 女神符號
    for cx in (16,56): d.rectangle([cx,10,cx+4,26],fill=(220,214,196)); d.polygon([(cx-1,10),(cx+2,4),(cx+5,10)],fill=FIRE1)
    save(im,"f_altar")
def anvil():
    im=img(44,32); d=ImageDraw.Draw(im)
    d.rectangle([10,20,34,30],fill=WOOD_XD)                                           # 木墩
    d.polygon([(6,12),(38,12),(34,18),(10,18)],fill=IRON_L); d.rectangle([16,18,28,22],fill=IRON)
    d.polygon([(2,10),(14,10),(12,14),(4,14)],fill=IRON)                              # 角
    save(im,"f_anvil")
def rack():   # 武具/工具架（靠牆）
    im=img(50,58); d=ImageDraw.Draw(im)
    d.rectangle([2,4,47,54],fill=WOOD_D); d.rectangle([4,6,45,52],fill=WOOD_XD)
    d.rectangle([10,8,14,50],fill=IRON_L); d.polygon([(9,8),(15,8),(12,2)],fill=IRON_L) # 劍
    d.rectangle([24,10,27,50],fill=WOOD); d.polygon([(20,10),(31,10),(25,4)],fill=IRON) # 斧/矛
    d.rectangle([36,12,40,50],fill=IRON); d.ellipse([33,6,43,16],outline=IRON_L,width=2)
    save(im,"f_rack")
def plant():
    im=img(32,40); d=ImageDraw.Draw(im)
    d.rectangle([8,26,24,38],fill=(150,96,60)); d.rectangle([8,26,24,29],fill=(178,120,78))  # 盆
    for cx,cy,r in [(16,16,11),(9,20,7),(23,20,7),(16,9,8)]: d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=CLOTH_G)
    d.ellipse([12,12,20,20],fill=(96,150,98))
    save(im,"f_plant")
def board2():   # 公會委託板
    im=img(60,58); d=ImageDraw.Draw(im)
    d.rectangle([2,6,57,52],fill=WOOD_D); d.rectangle([5,9,54,49],fill=(196,176,132))
    import random
    for px_,py_ in [(10,14),(30,13),(12,32),(34,31)]:
        random.seed(px_+py_); d.rectangle([px_,py_,px_+16,py_+12],fill=(230,224,206))
        d.rectangle([px_+7,py_-2,px_+9,py_],fill=CLOTH_R)   # 圖釘
    save(im,"f_board")

bed(); table(); chair(); stool(); counter(); shelf(); goods(); rug()
hearth(False); hearth(True); altar(); anvil(); rack(); plant(); board2()
print("furniture v12 done")
