# GDevelop AI 遊戲開發工作區

John（Team Lead）的個人遊戲開發工作區：用 Python 腳本直接組 GDevelop `game.json`，配合 gdevelop-mcp 工具驗證與預覽。主力專案是 **水晶戰記（crystal-quest）**——LPC 像素風 JRPG。

## 目錄地圖

```
GDevelop/
├── .env                     # GEMINI_API_KEY 等金鑰（已 gitignore，絕不入 repo/文件）
├── .claude/skills/gen-art/  # Gemini 產圖 skill（立繪/背景/地圖）
├── gdevelop-mcp/            # GDevelop MCP server（validate/preview 工具）
├── tools/
│   ├── lpc/                 # LPC 角色圖層庫（GPL/CC-BY-SA，合成行走圖用）
│   ├── lpc-terrain/         # LPC 地形圖集（圖磚/大樹）
│   ├── lpc-atlas1/ lpc-atlas2/  # 洞窟/建築素材圖集
│   └── Tiled（brew 裝在 /opt/homebrew/bin/tiled）
└── projects/
    ├── crystal-quest/       # ★ 主專案：開發指南 DEV_開發指南.md、路線圖 ROADMAP_開發計畫.md
    ├── overworld-demo/ rpg-battle/ my-first-game/ …  # 早期 demo，僅參考
```

## 環境要點（踩過的坑）

- **Node 一律用 22 絕對路徑** `/Users/john/.nvm/versions/node/v22.17.1/bin/node`（系統預設是 16，沒有 fetch）。
- **資源檔名不能有空格**（preview 靜態伺服器不解碼 %20）。
- 商店資產 JSON 用 curl 抓要帶 `-A "Mozilla/5.0"`（否則 403）：
  `https://resources.gdevelop-app.com/assets-database/assets/<id>.json`
- `preview_scene` 帶 `sceneName` 會**覆蓋 firstLayout**——該匯出目錄拿去跑 E2E 會跳過 Title 初始化（隊伍為空）。要跑 E2E 請用**不帶 sceneName** 的匯出。
- puppeteer 測試按鍵一律帶 `{delay:70}` 以上，否則 GDevelop 幀間漏按。

## 建置與驗證（crystal-quest）

```bash
cd projects/crystal-quest/scripts
python3 build_cq2.py && python3 art_v2.py && python3 art_v3_lpc.py   # 標準重建
# 角色/武器外觀變動時加跑：python3 art_v6_chars.py && python3 art_v5_battle.py && python3 build_cq2.py
# 敵人外觀變動時（先於 build 跑，產 lpc_src/）：python3 art_v8_foes.py && python3 art_v9_creatures.py
# NPC 走動/室內家具變動時（先於 build 跑，持久化平時免跑）：python3 art_v10_npcwalk.py && python3 art_v12_furniture.py
# 標題頁美術變動時（合成 menubg＋烘描邊選單字，先於 build 跑）：python3 art_v13_title.py
# 森林素材變動時（anokolisa 地面 atlas_forest＋多樹種 fst_*＋裝飾，先於 build 跑，來源 tools/anokolisa）：python3 art_v14_forest.py
```
之後用 gdevelop-mcp 的 `validate_project` + `preview_scene` 驗證；互動測試範本見開發指南。
build 內建迷宮連通性 assert，改地圖後 build 過 = 路通。

## 內容分工

- **John**：敘事與數值設計。填 `projects/crystal-quest/DESIGN_設計文件.md`（劇情/角色/地區）與 `CONTENT.json`（隊伍/技能/裝備/敵人/遭遇/節奏）。UI/戰鬥原型在 claude.ai/design 專案「Crystal Quest UI」，Tweaks 面板的選擇視為定案規格。
- **Agent**：讀上述文件實作。收到「照設計文件重建」= 讀 DESIGN 文件全面實作。

## Skills

- `/gen-art`：Gemini 產圖（立繪/戰鬥背景/區域地圖）。金鑰在 `.env`。像素小圖不適用——用 LPC 合成。

## 規範

- 公司級規範見 `~/.claude/CLAUDE.md`（繁體中文、Git 格式、機密不入 repo 等），本文件不重複。
- 素材授權混合（CC-BY-SA/GPL/CC0/OGA-BY/AI 生成），動素材必須同步更新 `projects/crystal-quest/CREDITS_素材授權.md`。
