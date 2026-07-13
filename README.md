# 水晶奇譚 Crystal Tales

GDevelop 製作的 LPC 像素風 JRPG——**芳蕾鎮篇**（序章＋第一章＋第二章）。
特色：ATB 戰鬥、六分頁選單、裝備／技能／道具、地圖寶箱、存檔、觸控虛擬搖桿、
六場景（Title／Town／Forest／Mine／Cave／Battle）與物件擺放式室內。

> 開發方式特殊：**用 Python 腳本直接組 `game.json`**（不在 GDevelop IDE 手拉），
> 再用 [gdevelop-mcp] 工具 validate／preview。主專案在 [`projects/crystal-quest/`](projects/crystal-quest/)。

## 目錄結構（本 repo）

```
GDevelop/
├── CLAUDE.md                 # 工作區開發規範（給協作者/AI）
├── .env.example              # 複製成 .env 填金鑰（.env 不入 repo）
├── .claude/skills/gen-art/   # Gemini 產圖 skill（立繪/背景/地圖）
├── tools/                    # 小型 LPC 圖集（terrain/atlas/creatures/dungeon）
│                             #   ⚠️ 完整角色產生器 tools/lpc（~780MB）未入 repo，見下
└── projects/crystal-quest/   # ★ 主專案
    ├── scripts/              # 建置腳本（build_cq2.py 等）＋ E2E
    ├── game.json             # 產物：由腳本生成，勿手改
    ├── assets/               # LPC 合成/程序繪的角色·地圖·戰鬥·UI·音效
    ├── DESIGN_設計文件.md      # 敘事/角色/地區設計
    ├── DEV_開發指南.md         # 內部架構與腳本矩陣
    ├── ROADMAP_開發計畫.md
    └── CREDITS_素材授權.md      # ★ 素材授權標註（混合 CC-BY-SA/GPL/CC0/OGA-BY/AI 生成）
```

## 環境需求

- **Node 22**（`gdevelop-mcp` 用；系統預設 16 無 `fetch`，`.mcp.json` 已指定絕對路徑）
- **Python 3 + Pillow**（`pip install pillow`；建置腳本用）
- GDevelop（預覽/匯出）

> ⚠️ 建置腳本目前內含**絕對路徑**（假設工作區在 `~/Projects/60_soho/30_Personal/GameCreator/GDevelop`）；
> 於其他機器 clone 後需調整腳本頂部的路徑常數。

## 建置與執行

```bash
cd projects/crystal-quest/scripts
# 標準重建（改動後必跑；內建迷宮連通性 assert，build 過＝路通）
python3 build_cq2.py && python3 art_v2.py && python3 art_v3_lpc.py
```

視變動另跑（皆在 `build_cq2.py` 之前，產物持久化、平時免跑）：

| 變動 | 先跑 |
|------|------|
| 角色/武器外觀 | `art_v6_chars.py`、`art_v5_battle.py`（跑完再跑一次 build） |
| NPC 走動 / 室內家具 | `art_v10_npcwalk.py`、`art_v12_furniture.py` |
| 敵人外觀 | `art_v8_foes.py`、`art_v9_creatures.py` |

之後用 `gdevelop-mcp` 的 `validate_project` ＋ `preview_scene` 驗證；互動測試範本見 `DEV_開發指南.md`。

## 首次設定

```bash
cp .env.example .env      # 填入 GEMINI_API_KEY（/gen-art 產圖用；不產圖可略）
```

**還原未入 repo 的大型工具**（僅在「重生角色/敵人美術」時需要；產好的美術已在 assets/）：

```bash
# LPC 角色產生器（~780MB）
git clone --depth 1 https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator tools/lpc
# gdevelop-mcp（GDevelop 驗證/預覽 MCP server）另行取得並 npm i && npm run build
```

## 素材授權

混合授權（CC-BY-SA 3.0 / GPL 3.0 / CC0 / OGA-BY 3.0 / AI 生成）。
逐項標註見 [`projects/crystal-quest/CREDITS_素材授權.md`](projects/crystal-quest/CREDITS_素材授權.md)——動素材務必同步更新。

[gdevelop-mcp]: https://github.com/ (工作區工具，另有自己的 repo；未納入本 repo)
