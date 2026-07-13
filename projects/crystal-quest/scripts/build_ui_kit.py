#!/usr/bin/env python3
"""Crystal Quest UI kit：把遊戲現行 UI 做成 claude.ai/design 預覽卡。
   輸出到 design/ui_kit/（assets 複製自遊戲實際素材；顏色/字級取自 build_cq2.py 實值）。
   推送用 DesignSync（Claude 執行）。改完設計後：改這支腳本或回報 token 變更→重生遊戲 UI。"""
import os, shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(_HERE)
OUT = f"{PROJ}/design/ui_kit"
A = f"{PROJ}/assets"
SCRATCH_E2E = "/private/tmp/claude-501/-Users-john-Projects-60-soho-30-Personal-GameCreator-GDevelop/3ce492e9-94cd-4d02-abd6-73f8a4230a52/scratchpad/e2e"

os.makedirs(f"{OUT}/assets", exist_ok=True)
COPY = {
    f"{A}/ui/panel.png": "panel.png",
    f"{A}/ui/panel_light.png": "panel_light.png",
    f"{A}/ui/btn.png": "btn.png",
    f"{A}/ui/cursor.png": "cursor.png",
    f"{A}/ui/overlay.png": "overlay.png",
    f"{A}/ui/menubg.png": "menubg.png",
    f"{A}/ui/battlebg.png": "battlebg.png",
    f"{A}/ui/face_ludo.png": "face_ludo.png",
    f"{A}/ui/face_marin.png": "face_marin.png",
    f"{A}/ui/face_aaron.png": "face_aaron.png",
    f"{A}/ui/region_map.png": "region_map.png",
    f"{A}/battle/hero_ludo_f0.png": "hero_ludo.png",
    f"{A}/battle/Goblin_Idle_1.png": "goblin.png",
    f"{SCRATCH_E2E}/e_town_lpc_buildings.png": "bg_town.png",
}
for src, dst in COPY.items():
    if os.path.exists(src): shutil.copy(src, f"{OUT}/assets/{dst}")
    else: print("skip missing", src)

# ---- 遊戲內實際 tokens（來源：build_cq2.py）----
TOKENS = {
    "顏色": [
        ("文字主色", "#FFFFFF", "所有內文"),
        ("文字描邊", "#0A0A14", "outline 2px"),
        ("強調金", "#FFE178", "HUD 金幣/選單標題/名字"),
        ("選取黃", "#FFEB78", "游標所在列/指令"),
        ("目標綠", "#AAE6AA", "HUD 目標列"),
        ("提示紫灰", "#AAB4DC", "操作提示列"),
        ("數值青", "#AADCEB", "角色頁衍生屬性列"),
        ("治療綠", "#78E68C", "我方目標選取"),
        ("失效灰", "#788296", "不可用/未解鎖"),
        ("警示紅", "#FF9696", "戰敗/確認警告"),
        ("場景底色", "#141822", "World 場景背景"),
        ("戰鬥底色", "#0A0C0F", "Battle 場景背景"),
    ],
    "字級": [
        ("92", "標題 Logo（水晶戰記）"),
        ("64", "戰鬥結算標題（勝利！）"),
        ("38", "Banner 事件橫幅"),
        ("30", "選單標題/戰鬥訊息列"),
        ("28", "對話內文/戰鬥指令"),
        ("26", "對話名字/選單分頁"),
        ("22", "選單內容列/HUD 目標"),
        ("20", "HUD/提示列"),
    ],
}

FONT = '"Noto Sans TC",system-ui,sans-serif'
BASE_CSS = f"""
  html,body{{margin:0;padding:0;background:#0d0f16;}}
  *{{box-sizing:border-box;}}
  .wrap{{width:640px;height:360px;overflow:hidden;border-radius:6px;}}
  .stage{{width:1280px;height:720px;position:relative;transform:scale(.5);transform-origin:top left;
         font-family:{FONT};font-weight:700;}}
  .px{{image-rendering:pixelated;}}
  .panel{{position:absolute;background-image:url(./assets/panel.png);background-size:100% 100%;}}
  .t{{position:absolute;color:#fff;white-space:pre;line-height:1.25;
      text-shadow:-2px 0 #0a0a14,2px 0 #0a0a14,0 -2px #0a0a14,0 2px #0a0a14,
                  -2px -2px #0a0a14,2px -2px #0a0a14,-2px 2px #0a0a14,2px 2px #0a0a14;}}
"""

def card(name, group, subtitle, body, extra_css="", wrap=True):
    inner = f'<div class="wrap"><div class="stage">{body}</div></div>' if wrap else body
    return (f'<!-- @dsCard group="{group}" name="{name}" subtitle="{subtitle}" -->\n'
            f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{BASE_CSS}{extra_css}</style></head><body>{inner}</body></html>')

W = {}

# ================= tokens =================
sw = "".join(
    f'<div class="sw"><div class="chip" style="background:{hexv}"></div>'
    f'<div class="lbl"><b>{n}</b><span>{hexv}</span><i>{use}</i></div></div>'
    for n, hexv, use in TOKENS["顏色"])
ty = "".join(f'<div class="tyrow"><span class="sz" style="font-size:{int(s)*0.55}px">水晶戰記 Aa 123</span>'
             f'<span class="meta">{s}px — {use}</span></div>' for s, use in TOKENS["字級"])
assets_strip = "".join(
    f'<div class="as"><img class="px" src="./assets/{f}" style="height:{h}px"><span>{lbl}</span></div>'
    for f, h, lbl in [("panel.png", 60, "panel 面板(拉伸)"), ("btn.png", 44, "btn 按鈕"),
                      ("cursor.png", 40, "目標游標"), ("face_ludo.png", 72, "立繪 144px"),
                      ("hero_ludo.png", 84, "戰鬥角色"), ("goblin.png", 64, "敵人(原生16px)")])
W["tokens.html"] = card("Tokens：色彩／字級／基礎素材", "Tokens", "取自 build_cq2.py 的遊戲實值", f"""
<div style="padding:20px;font-family:{FONT};color:#e8e8f2;max-width:640px">
  <h3 style="margin:0 0 10px;color:#FFE178">色彩</h3>
  <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:6px 14px">{sw}</div>
  <h3 style="margin:16px 0 8px;color:#FFE178">字級（遊戲內 px）</h3>{ty}
  <h3 style="margin:16px 0 8px;color:#FFE178">基礎素材</h3>
  <div style="display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap">{assets_strip}</div>
  <p style="color:#AAB4DC;font-size:12px">字型目前為引擎預設；候選：Fusion Pixel Font（開源繁中像素字型）。</p>
</div>""", extra_css="""
  .sw{display:flex;gap:8px;align-items:center}.chip{width:34px;height:34px;border-radius:4px;border:1px solid #333a4c;flex:none}
  .lbl{display:flex;flex-direction:column;font-size:12px}.lbl b{font-size:13px}.lbl span{color:#8f97ad}.lbl i{color:#6c7488;font-style:normal;font-size:11px}
  .tyrow{display:flex;align-items:baseline;gap:12px;margin:2px 0}.sz{color:#fff;white-space:nowrap}.meta{color:#8f97ad;font-size:12px}
  .as{display:flex;flex-direction:column;gap:4px;font-size:11px;color:#8f97ad;align-items:center}
""", wrap=False)

# ================= HUD =================
W["hud.html"] = card("HUD（大地圖）", "世界 UI", "隊伍狀態/目標/金幣+選單鍵", f"""
<img class="px" src="./assets/bg_town.png" style="position:absolute;width:1280px;height:720px;filter:brightness(.55)">
<div class="t" style="left:20px;top:12px;font-size:20px">路德 Lv2 126/134　瑪琳 Lv1 70/70</div>
<div class="t" style="left:20px;top:44px;font-size:22px;color:#AAE6AA">▶ 討伐東之森深處的哥布林頭目</div>
<div class="t" style="left:900px;top:12px;font-size:20px;color:#FFE178">〈哥布林剋星〉　金幣 337　[M]選單</div>
""")

# ================= 對話框 =================
W["dialog.html"] = card("對話框＋立繪", "世界 UI", "說話者立繪/名字金/內文28px/▽翻頁", f"""
<img class="px" src="./assets/bg_town.png" style="position:absolute;width:1280px;height:720px;filter:brightness(.55)">
<img class="px" src="./assets/face_marin.png" style="position:absolute;left:70px;top:388px;width:144px;height:144px">
<div class="panel" style="left:60px;top:540px;width:1160px;height:160px"></div>
<div class="t" style="left:90px;top:556px;font-size:26px;color:#FFE178">瑪琳</div>
<div class="t" style="left:90px;top:596px;font-size:28px">一個人？想得美。要去，就一起去。　▽</div>
""")

# ================= 選單（角色頁） =================
menu_rows = [
    ("路德　探索者　Lv2　EXP 18/46　HP 126/134　MP 33/33", "#FFFFFF"),
    ("物攻 24　魔攻 8　物防 10　魔防 3　閃避 9　會心 7.2%", "#AADCEB"),
    ("力量 13　敏捷 7　智力 5　屬性點 3（1=力 2=敏 3=智）", "#FFEB78"),
    ("── 技能（技能點 1・Enter 升級）／ 裝備（Enter 更換）──", "#FFFFFF"),
    ("▶ 強力斬　Lv2/10　MP3　威力 x1.15", "#FFEB78"),
    ("　 疾風刺　Lv1/10　MP4　威力 x1.00", "#EBEBF5"),
    ("　 武器：鐵劍（物攻+6）", "#EBEBF5"),
    ("　 防具：旅行衣（物防+2）", "#EBEBF5"),
    ("　 飾品：—", "#EBEBF5"),
]
rows_html = "".join(
    f'<div class="t" style="left:200px;top:{176+i*28}px;font-size:22px;color:{c}">{t}</div>'
    for i, (t, c) in enumerate(menu_rows))
W["menu.html"] = card("選單：角色頁", "世界 UI", "五分頁/完整屬性/技能+裝備同列選單", f"""
<img class="px" src="./assets/bg_town.png" style="position:absolute;width:1280px;height:720px;filter:brightness(.45)">
<div class="panel" style="left:140px;top:80px;width:1000px;height:520px"></div>
<div class="t" style="left:180px;top:100px;font-size:30px;color:#FFE178">選單</div>
<div class="t" style="left:420px;top:104px;font-size:26px">【角色】　 道具 　 地圖 　 稱號 　 系統</div>
{rows_html}
<img class="px" src="./assets/face_ludo.png" style="position:absolute;left:940px;top:150px;width:144px;height:144px">
<div class="t" style="left:180px;top:556px;font-size:20px;color:#AAB4DC">↑↓ 選擇　Enter 升技能/換裝備　1/2/3 屬性配點　Esc 返回　　金幣 337</div>
""")

# ================= 戰鬥 =================
W["battle.html"] = card("戰鬥 UI", "戰鬥 UI", "訊息列/指令2x2/隊伍狀態/目標游標", f"""
<img class="px" src="./assets/battlebg.png" style="position:absolute;width:1280px;height:720px">
<img class="px" src="./assets/goblin.png" style="position:absolute;left:252px;top:202px;width:96px;height:96px">
<div class="t" style="left:200px;top:302px;font-size:20px;width:200px;text-align:center;color:#FFEB78">哥布林拾荒者</div>
<img class="px" src="./assets/cursor.png" style="position:absolute;left:352px;top:230px;width:40px;height:40px">
<img class="px" src="./assets/hero_ludo.png" style="position:absolute;left:1026px;top:100px;height:130px">
<div class="panel" style="left:40px;top:16px;width:1200px;height:62px"></div>
<div class="t" style="left:60px;top:30px;font-size:30px">選擇攻擊目標（←→ 切換、Enter 確定、Esc 返回）</div>
<div class="panel" style="left:40px;top:566px;width:520px;height:146px"></div>
<div class="panel" style="left:575px;top:566px;width:665px;height:146px"></div>
<div class="t" style="left:90px;top:596px;font-size:28px;color:#FFEB78">攻擊</div>
<div class="t" style="left:300px;top:596px;font-size:28px">技能</div>
<div class="t" style="left:90px;top:652px;font-size:28px">道具</div>
<div class="t" style="left:300px;top:652px;font-size:28px">逃跑</div>
<div class="t" style="left:592px;top:578px;font-size:21px;color:#FFEB78">路德 Lv2  HP 126/134  MP 33/33</div>
<div class="t" style="left:592px;top:612px;font-size:21px">瑪琳 Lv1  HP 70/70  MP 38/38</div>
""")

# ================= 勝利結算 =================
W["victory.html"] = card("勝利結算", "戰鬥 UI", "升級與習得技能通知/點數池提示", f"""
<img class="px" src="./assets/battlebg.png" style="position:absolute;width:1280px;height:720px">
<img src="./assets/overlay.png" style="position:absolute;width:1280px;height:720px">
<div class="t" style="left:340px;top:150px;width:600px;text-align:center;font-size:64px;color:#FFE178">勝　利！</div>
<div class="t" style="left:240px;top:260px;width:800px;text-align:center;font-size:28px">獲得 39 經驗值 · 30 金幣
路德 升級 Lv2！　習得『疾風刺』！
（獲得屬性點與技能點——在選單→角色 分配）</div>
<img class="px" src="./assets/btn.png" style="position:absolute;left:460px;top:600px;width:360px;height:84px">
<div class="t" style="left:600px;top:624px;font-size:30px">繼續</div>
""")

# ================= 標題 =================
W["title.html"] = card("標題畫面", "畫面", "Logo/開始按鈕/操作說明", f"""
<img class="px" src="./assets/menubg.png" style="position:absolute;width:1280px;height:720px">
<div class="t" style="left:240px;top:150px;width:800px;text-align:center;font-size:92px;color:#FFE178">水晶戰記</div>
<div class="t" style="left:240px;top:280px;width:800px;text-align:center;font-size:34px;color:#BEC8EB">— 芳蕾鎮篇 —</div>
<img class="px" src="./assets/btn.png" style="position:absolute;left:460px;top:410px;width:360px;height:90px">
<div class="t" style="left:566px;top:436px;font-size:36px">開始冒險</div>
<div class="t" style="left:240px;top:580px;width:800px;text-align:center;font-size:20px;color:#96A0C8">方向鍵移動 · 空白鍵交談/推進劇情 · M 開啟選單 · 戰鬥支援鍵盤與滑鼠</div>
""")

for fn, html in W.items():
    open(f"{OUT}/{fn}", "w").write(html)
print("ui_kit written:", len(W), "cards +", len(os.listdir(f'{OUT}/assets')), "assets →", OUT)
