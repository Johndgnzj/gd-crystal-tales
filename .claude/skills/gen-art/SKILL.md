---
name: gen-art
description: 用 Gemini API 生成水晶戰記的美術素材（NPC/角色立繪、戰鬥背景、區域地圖、標題圖、圖示）。當 John 說「產圖」「生成素材」「幫某角色畫立繪」「換戰鬥背景」等美術生成需求時使用。像素級小圖（行走圖、圖磚、敵人戰鬥圖）不適用本 skill——那些用 LPC 合成或商店素材。
---

# gen-art：Gemini 產圖管線

## 金鑰

`GEMINI_API_KEY` 在 **GDevelop 根目錄 `.env`**（已 gitignore）。不要把 key 寫進任何程式碼、文件、commit。腳本會自動往上層找 `.env`。

## 生成

```bash
python3 .claude/skills/gen-art/gen_image.py --type <類型> [--frame bust|full] --prompt "<描述>" --out <路徑>
```

模型 `gemini-2.5-flash-image`（自動退階 `gemini-2.0-flash-preview-image-generation`；429/503 自動重試）。
`--type` 會自動加上風格前綴，維持與現有素材一致的構圖約定：

| type | 長寬比 | 構圖約定 | 存放與後處理 |
|------|--------|----------|--------------|
| `face` | bust→16:9 / full→3:4 | 人物置中、中性深底(#20222a)、無文字；**不預設色調**（顏色由角色描述帶入）。`--frame bust`＝腰上半身（預設）／`--frame full`＝全身 | **半身**存 `projects/crystal-quest/design/faces/<Name>.png` → 在 `scripts/art_v7_faces.py` 名單加 `<Name>` 對映 → 跑該腳本自動偵測人物中心裁 144×144 成 `assets/ui/face_<id>.png`。**全身**存 `design/faces/<Name>_full.png`（不進 art_v7，另作立繪／室內大型前景用） |
| `battlebg` | 16:9 | 側視戰場、中景留空、地平線在上 1/3、無角色 | 縮到 640×360 存 `assets/ui/battlebg_<場景>.png`，在 build_cq2.py 的 Bg 物件動畫清單與 BATTLE_JS 的 BGMAP 註冊 |
| `map` | 16:9 | 鳥瞰地區圖、無文字 | 存 `design/` 或縮製後替換 `assets/ui/region_map.png` |
| `title` | 16:9 | 關鍵美術、無 logo 文字 | 縮 1280×720 替換 `assets/ui/menubg.png`（合成流程見 `scripts/art_v13_title.py`） |
| `icon` | 1:1 | 置中主體、深底、無字 | 視用途 |
| `building` | 1:1 | 45° 斜角像素建築外觀、洋紅底 #ff00ff 去背（地圖用，維持像素風不套水彩） | 去背後縮放置放於地圖 |
| `interior` | 4:3 | **水彩手繪滿版室內場景**（與立繪同套風格）、暖色、無角色、無文字 | 存 `assets/map/int_<key>.png` → build 走 `_clean_ext` 產 `intc_<key>.png` 作立繪＋選單式室內背景 |
| `raw` | 自訂 `--ar` | 無前綴 | — |

## 角色立繪風格（統一方向；2026-07-13 依 `design/ref/role-design-*` 定調）

目標＝**細緻手繪水彩感的日式 RPG 動畫插畫**（已內建進 `gen_image.py` 的 `type=face` 前綴）：
- **細線稿**：線條細、乾淨、有輕重變化——**非**粗黑描邊。
- **水彩／手繪感上色**：柔和漸層、透明水洗、淡紙紋；**非**平塗 cel 硬色塊、**非**半寫實厚塗、**非**像素、**非** 3D。
- **配色不鎖色系**：各角色的主色／輔色／瞳色由**角色設計**決定（見 `DESIGN_設計文件.md §3 角色` 與 `ART_PROMPTS.md §3`），彼此要有辨識度、避免全隊撞成同一色調。`face` 前綴只給中性打光與中性底，**顏色一律由角色描述句帶入**。
- 大而有神的眼睛、俊美臉；**年齡誠實**——該年輕就俊美年輕，該老就真的蒼老多皺。
- 華麗多層次的奇幻冒險者服裝：皮帶／扣具／肩甲／披風／金邊滾邊／繁複刺繡。
- 人物**置中**、自信有個性的姿態；中性深底 `#20222a`（純色，供 art_v7 抓人裁像；不帶色調以免蓋掉角色配色）。
- 一致性訣竅：同一批角色沿用同一句 `face` 前綴、只改「角色描述句」；不穩時補 `fine line art / watercolor / NOT pixel art / NOT 3D` 重生，寧可多生兩張挑。

**分鏡規則（`--frame`）**：
- **非主要角色** → 只產 `--frame bust`（腰上半身）。
- **主要角色** → 產 `--frame bust`（供 art_v7 裁 144px 頭像）＋ `--frame full`（全身立繪，另存 `<Name>_full.png`）各一張。
- 全身圖**不能**餵 art_v7（頭裁完會太小、且 portrait 會裁破）——頭像一律走半身圖。

**跨素材共用**：「細線稿＋水彩手繪」這套**技法**是人物立繪與**室內背景**（`type=interior`）共用的美術 DNA，兩者技法要一致（色調各自依角色／房間氛圍決定，不共用）。地圖用的像素建築外觀（`type=building`）維持像素風、不套水彩。

⚠️ **版權**：`design/ref/role-design-*` 是他方版權宣傳美術（Tales 系列等）——**僅作風格「方向」靈感，不臨摹其角色或畫作、不散布**；生成 prompt 內**不放** IP 名或畫師名（既避免臨摹版權作品，也避免模型把字畫進圖）。本 skill 只保留上面用自己的話寫的「文字風格描述」。這些參考圖不入 repo／散布（已於根目錄 `.gitignore` 排除 `design/ref/`）。

## 生成後必做

1. **檢視圖片**（Read 截圖確認構圖），不合格改 prompt 重生成——每次生成都會不同，寧可多生兩張挑。
2. 後處理照上表接回遊戲管線，然後跑 build 管線（見根目錄 CLAUDE.md）。
3. **授權標註**：在 `projects/crystal-quest/CREDITS_素材授權.md` 註明「AI 生成（Gemini），提示詞作者 John」。

## 邊界

- 生成式**不適合** 16-64px 像素素材（行走圖/圖磚/敵人小圖）：偽像素網格對不齊。用 `tools/lpc/` 圖層合成或 GDevelop 商店（見記憶與 DEV 指南）。
- prompt 一律描述畫面內容與風格，**不要放遊戲名或人名文字**（模型會把字畫進圖裡）。
- 免費額度有限，失敗先看 HTTP 429（配額）再重試。
