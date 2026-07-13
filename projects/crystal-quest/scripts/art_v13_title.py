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

# --- 立繪去背（新版立繪＝置中構圖＋中性藍灰底）---
# flood-fill 只挖「與邊界相連」的背景；人物內部即使有接近背景色的像素（髮間高光/冷灰）也不相連→保留實心，
# 不會像亮度鍵/純色距把頭髮挖成半透明。回傳去背後（未裁 bbox）的影像。
from PIL import ImageFilter
from collections import deque
def _cutout(im, tol=40):   # 容差調低：只挖「明顯是背景」者，避免滲進與底色相近的衣物/披風
    w,h=im.size; data=list(im.getdata())                   # 一次取出像素，索引 i=y*w+x（比 px[] 快）
    cs=[data[3*w+3],data[3*w+(w-4)],data[(h-4)*w+3],data[(h-4)*w+(w-4)]]   # 四角取樣＝背景色
    bg=tuple(sum(c[k] for c in cs)//4 for k in range(3))
    def isbg(i): d=data[i]; return abs(d[0]-bg[0])+abs(d[1]-bg[1])+abs(d[2]-bg[2])<=tol
    alpha=bytearray(b"\xff")*(w*h); seen=bytearray(w*h); dq=deque()
    for x in range(w):
        for i in (x,(h-1)*w+x):
            if not seen[i] and isbg(i): seen[i]=1; alpha[i]=0; dq.append(i)
    for y in range(h):
        for i in (y*w,y*w+w-1):
            if not seen[i] and isbg(i): seen[i]=1; alpha[i]=0; dq.append(i)
    while dq:
        i=dq.popleft(); x=i%w; y=i//w
        for j in ([i-1] if x>0 else [])+([i+1] if x<w-1 else [])+([i-w] if y>0 else [])+([i+w] if y<h-1 else []):
            if not seen[j] and isbg(j): seen[j]=1; alpha[j]=0; dq.append(j)
    al=Image.frombytes("L",(w,h),bytes(alpha)).filter(ImageFilter.GaussianBlur(0.6))  # 約 1px 抗鋸齒
    im.putalpha(al); return im
def _tightsave(im,out):
    bbox=im.getbbox()
    if bbox: im=im.crop(bbox)
    im.save(out)
# 室內「立繪＋選單」大型前景（半身圖去背；比例自然、依高度縮放錨右下）
def portrait(name):
    src=f"{PROJ}/design/faces/{name}.png"
    if os.path.exists(src): _tightsave(_cutout(Image.open(src).convert("RGBA")),f"{U}/portrait_{name}.png")
# 選單「故事」頁大型全身立繪（裁掉四周浮水印/白邊→去背→正規化到統一畫布，選單 sprite 尺寸一致好定位）
def menuart(name):
    src=f"{PROJ}/design/faces/{name}_full.png"
    if not os.path.exists(src): return
    im=Image.open(src).convert("RGBA"); w,h=im.size
    m=int(min(w,h)*0.045); im=im.crop((m,m,w-m,h-m))       # 去角落浮水印/白邊
    im=_cutout(im); bb=im.getbbox()
    if bb: im=im.crop(bb)
    CW,CH=520,800; TH=CH-20; sw=int(im.width*TH/im.height)  # 統一畫布 520x800
    if sw>CW-20: sw=CW-20; TH=int(im.height*sw/im.width)
    im=im.resize((sw,TH),Image.LANCZOS)
    cv=Image.new("RGBA",(CW,CH),(0,0,0,0)); cv.alpha_composite(im,((CW-sw)//2,CH-TH))  # 水平置中、底部對齊
    cv.save(f"{U}/menuart_{name}.png")
# 對話大立繪＋室內前景：所有有臉的角色都去背（半身、透明底、tight 裁切）
for _n in ["ludo","marin","aaron","tina","dora","sister","barton","gid","hank","martha","gray","mira","guard"]:
    portrait(_n)
for _n in ["ludo","marin","aaron"]: menuart(_n)   # 選單全身：主角三人
print("title v13 done: menubg + t_* + portrait_*(13) + menuart(ludo/marin/aaron)")
