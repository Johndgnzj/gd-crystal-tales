# 建置腳本
- `python3 build_cq2.py` — 讀 ../CONTENT.json 生成 game.json（地圖/場景/戰鬥/劇情）
- `python3 art_v2.py` — 精細版美術覆蓋（必須在 build 之後跑）
- `cq2_e2e.mjs` / smoke 測試 — puppeteer 自動通關（node 22 + 先用 preview_scene keepExport 匯出）
改 CONTENT.json 或劇情台詞（build_cq2.py 內 DLG/CUTS）後，依序跑上面兩支即可。
