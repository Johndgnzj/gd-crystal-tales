# 水晶戰記 開發路線圖（2026-07-12 起草）

> 給協作 Agent：認領一個 Track 開工前先讀根目錄 `CLAUDE.md` 與 `DEV_開發指南.md`。
> ⚠️ **並行衝突規則**：多個 Track 同時動 `build_cq2.py` 會互相蓋寫——同一時間只允許一個
> 「引擎 Track」動這個檔；純資料（CONTENT.json）與純文件/美術 Track 可自由並行。
> 每個 Track 完成定義＝build 通過＋E2E/截圖驗證＋CREDITS/文件同步＋記憶更新。

## 總覽與建議並行批次

| 批次 | 可同時進行 | 理由 |
|------|-----------|------|
| 第一批 | A 劇情草稿（純文件）＋ C 道具裝備資料設計（CONTENT+文件）＋ E 小鎮豐富化（town 段+美術） | 三者檔案不重疊 |
| 第二批 | D 商店系統（引擎，吃 C 的資料）＋ B 觸控支援（輸入層） | C 定稿後 D 才能開工；B 與 D 都動 build_cq2.py→需協調或串行 |
| 第三批 | A 劇情實作（DLG/CUTS/新戰鬥）＋ G 存檔系統 | A 實作依賴 C/D 上線（委託獎勵發道具）＋劇情定稿 |

---

## ✅ Track A：第二章「重返礦山」劇情（2026-07-12 完成）

**已落地並 E2E 全流程驗證**（單場 puppeteer 從接委託打到回報，所有旗標/獎勵正確、零 pageerror）：
- 委託線：老葛雷 `ch1==3`→`ch2_take`(ch2=1)→礦山深處 `mine_truth` 過場→**狂暴洞熊精英戰**（`bear_dire` hp480/atk36/def16/spd8/allAttack、exp180/gold100，big 頂部血條）勝利→ch2=2＋掉『疾風靴』→回 Mine 播 `mine_after`→老葛雷 `ch2_report`(ch2=3)＋150G＋藥水×2。
- 支線A（米拉鏡草×3）：`mira_start`(送凝神耳環當訂金＋mira2=1)→東之森 3 個 Herb pickup→`mira_reward`(藥水×3)。
- 支線B（阿吉頭盔）：礦山深處 `RelicHelmet` pickup(relic=1＋miner_helmet)→老葛雷 `relic_turnin`(+100G)。
- 新增 `wolf`（野狼，Lv3-5，掉 wolf_hide；forest2/mine 遭遇組）＋ `bear_dire`；漢克鋪與吉德店移除 tier:2 商品。
- 稱號 t_miner/t_relic；Cave 深處落石訊息依 ch2 分流（≥2 露出第三章鉤子）；HUD 目標鏈接上 ch2。
- 修正既有 bug：緹娜 `ch1==3` 後會落到 `reg==1` 分支誤觸 `ch1_take` 把 ch1 重設回 1——已插入 ch2>=1/ch1==3 分支擋掉。

**兩個工程決策（偏離草稿處，已記錄）：**
1. **採用共用 flag-matcher（`matchWhen`）＋通用 `CFG.pickups` 原語**（草稿 8-7 建議案）：DLG/trigger/pickup 共用同一 `always`/`旗標==N`/`旗標>=N` 比對；trigger 加 `when` 閘門（`mine_truth` 綁 ch2>=1，序章 step0 不誤觸）。
2. **鎮北 Town→Mine 出口維持不上鎖**：草稿 8-7 建議 `when:"ch2>=1"`，但序章(step0)必須走此出口進礦山，上鎖會斷序章——故不採用；礦山高等遇敵＋隱藏 BearMark 已是天然軟閘門。

**（草稿→實作的落差）** 草稿接線用舊 `g_items` 單計數器，已全部改用現行 `g_itemInv` 背包 helper（invAdd）。`bear_dire` 數值採 John 定案（比草稿 hp260 更硬）。

<details><summary>原始範圍（保留供參）</summary>


**範圍**（依 DESIGN_設計文件.md 章節表）：
- 委託線：ch1==3 後老葛雷發第二章委託（調查礦工失蹤）→ 礦山深處事件
  「骷髏礦工＝失蹤的死者」揭露 cutscene → 洞穴深處 step 解鎖（現有「落石封住」觸發區改開放）
- 精英戰：洞熊（已有數值 hp90 級，需再平衡到 Lv5-8 帶）；章末銜接第三章食人魔
- 支線（候選，DESIGN 內）：米拉藥草×3、礦工的遺物（頭盔）
- 新旗標 `ch2`、新稱號、EXP pacing 已有 mine 帶（Lv5-8）
- 交付：DLG/CUTS 新條目、旗標機擴充、E2E 通關驗證

**John 輸入**：台詞可由 Agent 照現有文風起草→John 改；「洞熊 or 無 boss」二選一要定案。
**工作量**：草稿半天／實作 1 天。**衝突**：動 build_cq2.py（DLG/CUTS/cfg 段）。
</details>

## ✅ Track B：手機/平板觸控支援（2026-07-12 完成，虛擬搖桿方案）

**John 定案＝虛擬搖桿。** 已落地並 puppeteer 觸控 E2E 驗證（搖桿右移實測位移 +203px、BtnMenu 開關選單、PadR 切分頁皆通）：
- 左下**浮動虛擬搖桿**（追蹤單一觸控 id、knob 夾在半徑內、`b.simulateControl` 餵 TopDown 八方向）；右下**互動鈕**（＝空白鍵/OK）＋**≡ 選單鈕**（＝M）。
- 對話/過場**點任意處推進**。選單/商店：左下 **dpad(▲▼◀▶)＋✕返回**、右下 OK/≡；角色能力頁多三顆 **力/敏/智** 配點鈕。全部以「合成鍵餵給既有 keyHit/hit 流程」實作，鍵盤與觸控並存。
- 戰鬥觸控本就支援。座標：觸控按鈕與命中皆在 UI 圖層(預設相機、螢幕座標)，`im.getTouchX` 直接可用。
- ⚠️ 觸控按鈕在過場/對話時隱藏（BtnMenu/dpad），搖桿於 lock 時停用——測試觸控要先確保處於自由行動態。

<details><summary>原始範圍（保留供參）</summary>

**範圍**：
- 世界移動：二選一——(1) 虛擬搖桿（左下浮動搖桿+右下互動鈕，GDevelop 觸控已可用 getStartedTouchIdentifiers）；(2) 點地移動＋BFS 自動尋路（迷宮地圖 BLK 網格現成，路徑跟隨要寫）。**建議先做 (1)**，工作量小且迷宮手感好。
- 對話：點擊任意處推進（等同空白鍵）。
- 選單：分頁/列/裝備流程全部 insideObject 命中測試（戰鬥已有前例可抄）。
- 戰鬥：已支援滑鼠/觸控，補防禦鍵等新指令的命中即可。
- 專案屬性已是 landscape + adaptGameResolution ✓。
- 驗證：puppeteer touch 模擬 + 縮小視窗比例測試。

**John 輸入**：搖桿 vs 點地移動的偏好。
**工作量**：1 天。**衝突**：動 build_cq2.py（WORLD_JS 輸入層＋UI 物件）。
</details>

## Track C：道具與裝備完整設計（說明/屬性/價格）

**範圍**（資料為主，選單原型 cq_data.js 已有 John 認可的草稿方向）：
- `items` 擴充：藥草/上級藥草/魔力草/解毒草/復活羽毛/帳篷（消耗品）＋哥布林牙/狼皮/鐵礦石/水晶碎片（素材，敵人掉落）＋公會登錄證等（重要物品）。每項：name/desc/cat/effect/buy/sell。
- `equipment` 補完：現有 14 件全部加 `desc` 與 `buy/sell`；新增第二章位階（鋼劍/鎖子甲/法師袍/守護墜飾等，參考原型數值）。
- **引擎前置**（可與資料同 PR）：`g_items` 從單一計數器改 `g_itemInv`（id→數量 JSON），選單道具頁與戰鬥道具選單改列多項目、素材/重要分類。
- 敵人掉落表：enemies 加 `drops:[{id,rate}]`。
- 交付：CONTENT.json 定稿＋一份《道具裝備一覽》文件供 John 審數值。

**John 輸入**：價格與效果數值定案（Agent 先按「藥水 60HP=30G」基準推整條曲線）。
**工作量**：資料半天＋引擎改造 1 天。**衝突**：引擎部分動 build_cq2.py。

## Track D：商店系統（道具屋/裝備屋）

**範圍**（Design 選單原型的「商店」分頁已是完整 spec：買/賣頁籤、列表+價格、金幣顯示、確認）：
- 吉德道具店（消耗品）＋漢克鐵匠鋪（武具）各自商品表 `CONTENT.shops`。
- 對話 action `open_shop:<id>` → 商店 UI（複用選單 MRow/血條/高亮元件）。
- 買：金幣扣款進背包；賣：素材/裝備回收（sell 價）。
- 金幣經濟閉環：委託報酬/掉落 → 商店消費（目前金幣無用途）。
- 依賴：**C 的價格與 g_itemInv 先行**。
- 驗證：E2E 買藥水/賣素材/金幣變動。

**John 輸入**：商品清單與解鎖時機（例：鐵匠第二章進貨鋼劍）。
**工作量**：1 天。**衝突**：動 build_cq2.py（WORLD_JS 選單段）。

## Track E：初始小鎮豐富化

**範圍**：
- 依 `design/芳蕾鎮區域地圖.png`：鎮中央加**河流與石橋**（水磚已有）、廣場攤位/花圃/路燈/曬衣繩/木箱酒桶（LPC atlas2 有現成組件）。
- **NPC 生活感**：鎮民簡單巡走（2-3 點來回，TopDown 或直接座標插值）、貓/狗/雞（LPC 有動物素材可查）。
- 告示板互動：顯示當前委託與建議等級（讀 pacing）。
- 建築內部（旅店/公會室內場景）**列為選配**——工作量大，先不做。
- 驗證：截圖審美＋碰撞不擋主線動線（出入口 E2E）。

**John 輸入**：無必須；有想要的地標可提。
**工作量**：1 天。**衝突**：動 build_cq2.py（town 段）＋art 腳本。

## 追加建議（未在需求內、價值高）

| Track | 內容 | 為什麼 |
|-------|------|--------|
| ✅ **G 存檔系統**（2026-07-12 完成） | localStorage 存 g_flags/party/eqInv/itemInv/gold/chests＋場景座標；**自動存檔**（進場景/對話動作/pickup/寶箱/買賣）；Title「繼續冒險」載入回存檔場景、「重新開始」清存檔。E2E 驗證存→重載→繼續狀態一致（Mine/gold777/ch2:1）。室內存門口外避免卡牆。 | 進度持久化，手機版（B）必備 |
| F 技能樹 | Design 原型已有完整 spec（前置條件/被動/守護/降攻 debuff） | 第二章成長系統；戰鬥機制已 ATB 化，容易掛新技能種類 |
| H 狀態異常 | 中毒/麻痺＋解毒草（C 有道具）＋神殿解異常兌現設計 | DESIGN 已寫「神殿=免費解狀態異常」，目前是空話 |
| I 平衡自動化 | 無頭自動打完序章～ch1，輸出等級/金幣/戰鬥時長曲線 | pacing 參數調整就不用人肉試玩 |

## Track J：45° 可進入房子＋就地室內（2026-07-12 新增，John 指定方向）

**視覺**：小鎮六棟建築改用 **45° 斜角像素風外觀**（gen-art 生成→洋紅去背→縮放置放）。
已驗證：pixel 風格外觀合成到現有像素小鎮完全契合（scratchpad/town_composite.png）；插畫風會與地圖打架，不採用。

**進屋機制（同場景就地切換，非換場景）**：
- 每棟建築門口一個觸發區；玩家踏上/按空白鍵 → `st.inside = 建築id`。
- 隱藏所有戶外建築外觀＋戶外 NPC/props（或整個戶外層），顯示該建築的**室內大圖**（斜角剖面房間，如 scratchpad/interior.png 風格），放置室內 NPC＋家具，玩家移動限制在室內地板邊界內。
- 走到室內門/邊緣 → 還原（st.inside=null）、外觀重現、玩家回到門口。
- 純狀態覆蓋：一個 Interior 大圖物件＋室內碰撞邊界＋室內 NPC 物件，toggle 顯示。**是 WORLD_JS 引擎工作，排在 build_cq2.py 空出後**。

**素材**：外觀 6 棟＋室內 6 間，各一張 gen-art（洋紅底去背）。gen-art 加一個 `building` type 前綴（45°斜角、洋紅底、無文字）較穩定。
**取代**：E 剛做的程式/LPC 平面建築；E 的河流/攤位/告示板/母雞保留。

## ✅ Track K／#6：地牢圖磚接縫一致性（2026-07-12 完成，手工像素、非 gen-art）

已重做 art_v2.py 的地牢地板：新增 **toroidal `wrap_dither`**（blob 跨格邊 wrap 到對邊→單格 32px 真正無縫平鋪）＋裂縫改內側不觸邊；rockfloor/gravel（礦坑暖中性灰）與 cavefloor/cavedark（洞穴冷暗灰）統一為**同一套地下岩石家族**（礦坑→洞穴讀起來是連續變深的地底）。截圖確認礦坑地板無接縫、無明顯格狀重複。gravel（遇敵）保留較亮粗糙以便辨識但對比降低。

<details><summary>原始分析（保留供參）</summary>

**問題**：圖磚相鄰時要無縫、地圖↔地下礦坑材質要連續一致。
**根因**：LPC terrain（草/路）本身無縫；但 art_v2 自繪的地牢地板（rockfloor/gravel/cavefloor/cavedark）是逐格 dither，重複鋪排會有接縫/重複感；mine 與 cave 目前地板材質不完全統一。
**做法（像素圖磚重製，不是 gen-art）**：
1. 稽核各圖磚 32px 邊緣是否 wrap（左右/上下接得起來）。
2. 自繪地牢地板改成 edge-matched 可平鋪版本，或改用 LPC base_out 的無縫岩石/洞穴地板。
3. mine 與 cave 共用同一套地下岩石 tileset，讓「礦山外圍→洞穴深處」讀起來是連續的地底。
4. autotile 邊界（路/土的九宮格）已 OK，重點在大面積填充磚。
</details>

## ✅ John 定案（2026-07-12，餵給 A-impl）

1. **章末精英戰洞熊再強一點**：`bear_dire` 比草稿(hp260/atk28/def12)更硬——建議 hp480/atk36/def16/spd8/allAttack、exp180/gold100，做成 Lv6-8 需練級＋補品才過的牆。
2. **加狼**：新增「狼」敵人當 `wolf_hide` 來源（GDevelop 商店抓 wolf 精靈，比照其他敵人下載幀+描邊；真的沒有再退而求其次 recolor 既有並註明）。狼掉 wolf_hide，放進森林深處/礦山遭遇組（Lv3-5 級）。
3. **tier:2 裝備不在初始鎮賣**：從漢克鐵匠鋪 sell 清單移除鋼劍等 tier:2；它們屬於**未來的新城鎮**（見 Track L）。芳蕾鎮鐵匠只賣 tier1。
4. **報酬**：主線 150G＋藥水×2 沿用；支線獎勵照草稿。
5. **價格**：照 `道具裝備一覽.md` 推導值，不調。

## Track L：新城鎮（大城/第二階段，之後再做）

第二章后玩家前往的新城鎮，販售 tier:2 及更高階裝備。需要：新場景 Town2、建築（可沿用 45° 房子 gen-art 流程）、NPC、商店（tier:2+）、劇情銜接。**尚未開工**，待第二章上線後再規劃。

## 認領方式

在對話中指名 Track（例：「做 Track C+D」）。動 `build_cq2.py` 的 Track 同時只跑一個；
純文件/資料 Track 可交給另開的 session 或 subagent 並行。
