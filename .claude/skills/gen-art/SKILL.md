---
name: gen-art
description: 用 Gemini API 生成水晶戰記的美術素材（NPC/角色立繪、戰鬥背景、區域地圖、標題圖、圖示）。當 John 說「產圖」「生成素材」「幫某角色畫立繪」「換戰鬥背景」等美術生成需求時使用。像素級小圖（行走圖、圖磚、敵人戰鬥圖）不適用本 skill——那些用 LPC 合成或商店素材。
---

# gen-art：Gemini 產圖管線

## 金鑰

`GEMINI_API_KEY` 在 **GDevelop 根目錄 `.env`**（已 gitignore）。不要把 key 寫進任何程式碼、文件、commit。腳本會自動往上層找 `.env`。

## 生成

```bash
python3 .claude/skills/gen-art/gen_image.py --type <類型> --prompt "<描述>" --out <路徑>
```

模型 `gemini-2.5-flash-image`（自動退階 `gemini-2.0-flash-preview-image-generation`；429/503 自動重試）。
`--type` 會自動加上風格前綴，維持與現有素材一致的構圖約定：

| type | 長寬比 | 構圖約定 | 存放與後處理 |
|------|--------|----------|--------------|
| `face` | 16:9 | 人物佔左 1/3、深藍底(#141822)、右側星光、無文字 | 存 `projects/crystal-quest/design/faces/<Name>.png` → 在 `scripts/art_v7_faces.py` 的名單加上 `<Name>` 對映 → 跑該腳本自動偵測人物中心裁 144×144 成 `assets/char/face_<id>.png` |
| `battlebg` | 16:9 | 側視戰場、中景留空、地平線在上 1/3、無角色 | 縮到 640×360 存 `assets/ui/battlebg_<場景>.png`，在 build_cq2.py 的 Bg 物件動畫清單與 BATTLE_JS 的 BGMAP 註冊 |
| `map` | 16:9 | 鳥瞰地區圖、無文字 | 存 `design/` 或縮製後替換 `assets/ui/region_map.png` |
| `title` | 16:9 | 關鍵美術、無 logo 文字 | 縮 1280×720 替換 `assets/ui/menubg.png` |
| `icon` | 1:1 | 置中主體、深底、無字 | 視用途 |
| `raw` | 自訂 `--ar` | 無前綴 | — |

## 生成後必做

1. **檢視圖片**（Read 截圖確認構圖），不合格改 prompt 重生成——每次生成都會不同，寧可多生兩張挑。
2. 後處理照上表接回遊戲管線，然後跑 build 管線（見根目錄 CLAUDE.md）。
3. **授權標註**：在 `projects/crystal-quest/CREDITS_素材授權.md` 註明「AI 生成（Gemini），提示詞作者 John」。

## 邊界

- 生成式**不適合** 16-64px 像素素材（行走圖/圖磚/敵人小圖）：偽像素網格對不齊。用 `tools/lpc/` 圖層合成或 GDevelop 商店（見記憶與 DEV 指南）。
- prompt 一律描述畫面內容與風格，**不要放遊戲名或人名文字**（模型會把字畫進圖裡）。
- 免費額度有限，失敗先看 HTTP 429（配額）再重試。
