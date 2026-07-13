#!/usr/bin/env python3
"""標題頁 v13：新手繪森林 title_new 當背景 ＋ 合成現有 logo（logo_hei：徽記＋水晶奇譚＋CRYSTAL TALE）
   → assets/ui/menubg.png；並烘出「無框、有描邊」的選單文字 PNG（開始遊戲/繼續冒險/重新開始）→ assets/ui/。
   須在 build_cq2.py 之前跑（ui/*.png 由 build 掃描註冊）。"""
import os
from PIL import Image, ImageDraw, ImageFont
_HERE=os.path.dirname(os.path.abspath(__file__)); PROJ=os.path.dirname(_HERE)
A=f"{PROJ}/assets"; D=f"{PROJ}/design/title"; U=f"{A}/ui"

def cjk(px):
    for fp in ["/System/Library/Fonts/STHeiti Medium.ttc","/System/Library/Fonts/PingFang.ttc",
               "/System/Library/Fonts/Hiragino Sans GB.ttc","/Library/Fonts/Arial Unicode.ttf"]:
        try: return ImageFont.truetype(fp,px)
        except Exception: pass
    return ImageFont.load_default()

# --- 標題背景：森林手繪圖（含主角淡彩虹剪影朝水晶走）+ logo（沿用既有徽記/水晶奇譚字樣）---
SRC_BG = "tv_a.png"   # John 選定的標題變體（可換 tv_b/tv_c/title_new）
bg=Image.open(f"{D}/{SRC_BG}").convert("RGBA").resize((1280,720),Image.LANCZOS)
logo=Image.open(f"{D}/logo_hei.png").convert("RGBA")
lw=470; lh=round(logo.height*lw/logo.width); logo=logo.resize((lw,lh),Image.LANCZOS)
bg.alpha_composite(logo,((1280-lw)//2,10))
bg.convert("RGB").save(f"{U}/menubg.png")

# --- 無框、有描邊的選單文字（John：不要框、但文字本身有邊線；描邊調細）---
def txt(s,path,px,fill=(247,237,212),stroke=(22,26,44),sw=3):
    f=cjk(px); m=ImageDraw.Draw(Image.new("RGBA",(4,4)))
    l,t,r,b=m.textbbox((0,0),s,font=f,stroke_width=sw); w,h=r-l,b-t; pad=10
    im=Image.new("RGBA",(w+pad*2,h+pad*2),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.text((pad-l,pad-t),s,font=f,fill=fill,stroke_width=sw,stroke_fill=stroke)  # Pillow stroke＝文字描邊(細)
    im.save(path)
txt("開始遊戲",f"{U}/t_start.png",58)
txt("繼續冒險",f"{U}/t_cont.png",48)
txt("重新開始",f"{U}/t_restart.png",48)
txt("開始新遊戲",f"{U}/t_new.png",48)   # 無存檔時用（取代「重新開始」，語意較對）
txt("交談",f"{U}/t_talk.png",44)         # 室內立繪+選單指令
txt("離開",f"{U}/t_leave.png",44)

# --- 室內「立繪＋選單」用：從 design/faces 半身圖去深藍底（亮度鍵＋羽化）當室內大型前景角色 ---
from PIL import ImageFilter
def portrait(name):
    src=f"{PROJ}/design/faces/{name}.png"
    if not os.path.exists(src): return
    im=Image.open(src).convert("RGBA"); w,h=im.size
    im=im.crop((0,0,int(w*0.46),h)); w,h=im.size          # 人物在左側，裁左 46%
    px=im.load(); al=Image.new("L",(w,h),0); ap=al.load()
    for y in range(h):
        for x in range(w):
            r,g,b,a=px[x,y]; lum=(r*30+g*59+b*11)//100
            ap[x,y]=0 if lum<=22 else (255 if lum>=44 else int((lum-22)*255/22))
    al=al.filter(ImageFilter.GaussianBlur(2))              # 羽化邊緣，柔和融入房間
    im.putalpha(al)
    im.save(f"{U}/portrait_{name}.png")
for _n in ["tina"]: portrait(_n)   # 先做公會（緹娜）；其餘棟核可後再補
print("title v13 done: menubg + t_start/t_cont/t_restart/t_new + portrait_tina")
