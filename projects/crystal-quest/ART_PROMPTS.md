# 產圖 Prompt 集（世界地圖 / 芙瑞達大陸）

> 用法：直接複製英文區塊貼進 Midjourney / DALL-E / Stable Diffusion。
> 通用建議：
> - **不要讓 AI 畫地名文字**（會亂碼）——prompt 都寫了 no text；地名之後用繪圖軟體疊字，或丟回給 Claude 標。
> - 世界地圖建議比例 16:9 或 3:2；大陸地圖 4:3 或 1:1。Midjourney 加 `--ar 16:9`。
> - 想要系列風格一致：Midjourney 用同一張當 `--sref`；GPT-4o/DALL-E 在同一對話串裡連續生成。

---

## 1. 世界地圖（七大陸）

### 1-A 手繪奇幻地圖版（設定集/宣傳用）

```
Hand-drawn fantasy world map on aged parchment, ink linework with soft watercolor wash,
a vast ocean world with SEVEN distinct continents scattered across the sea:
(1) a large temperate continent of green plains, farmland and gentle hills,
(2) a harsh northern continent of black iron mountains and storm-battered sea cliffs,
(3) a continent of towering wind-carved peaks and deep canyons, perpetual gales,
(4) an ancient forest continent completely veiled in white mist,
(5) a southern savanna peninsula with tribal wilderness,
(6) a tropical archipelago of rainforest islands connected like a chain,
(7) a lake-dotted continent with clusters of small floating islands,
decorative compass rose, subtle sea serpent illustrations in the ocean,
classic JRPG world map cartography, warm muted colors, highly detailed, no text, no labels
```

中文對照：羊皮紙手繪世界地圖，海洋世界上散布七塊大陸——溫帶平原（芙瑞達/人族）、
北方鐵黑山脈風暴海崖（比爾/矮人）、強風峽谷高峰（亞力士/翼人）、迷霧古森（裘恩/精靈）、
南方莽原半島（魏恩/獸人）、熱帶雨林島鏈（傑魯得/森人）、湖泊浮島（郝麗/妖精），
裝飾羅盤、海怪插畫，無文字。

### 1-B 像素遊戲風版（遊戲內世界地圖畫面）

```
16-bit SNES JRPG world map, top-down pixel art, deep blue ocean with seven distinct
pixel continents: green plains continent, dark iron mountain continent in the north,
windy canyon peaks continent, mist-covered forest continent, southern savanna peninsula,
tropical island chain, lake continent with tiny floating islands,
classic Final Fantasy / Dragon Quest overworld style, crisp pixels, limited color palette,
no text, no UI
```

---

## 2. 芙瑞達大陸（起始大陸・區域地圖）

### 2-A 手繪奇幻地圖版

```
Hand-drawn fantasy regional map on aged parchment, ink and watercolor cartography,
a temperate continent region: in the CENTER a small riverside town with a stone bridge,
surrounded by farmland; to the EAST a wide green forest with wildlife;
to the NORTH barren rocky hills with abandoned mine entrances, old wooden rail tracks
and dark cave mouths; to the SOUTH a paved trade road winding toward a distant large
walled city on the horizon; to the WEST a dense ominous forest wall shrouded in thick fog;
small illustrative icons for trees, mountains and buildings, dotted travel paths,
decorative border, classic JRPG region map style, warm colors, no text, no labels
```

中文對照：中央河畔小鎮（石橋+農田）、東=綠色大森林、北=荒丘+廢棄礦坑口+舊軌道+洞穴、
南=通往遠方城牆大城的官道、西=濃霧封鎖的黑森林邊界。插畫式圖標、虛線旅路、裝飾邊框，無文字。

### 2-B 像素遊戲風版

```
16-bit JRPG regional overworld map, top-down pixel art: a small riverside town with
stone bridge in the center surrounded by farm fields, big green forest on the east side,
rocky barren hills with mine entrances and cave openings in the north, a long paved road
leading south toward a big walled city at the map edge, a dark fog-covered forest
blocking the west edge, dirt paths connecting all areas, SNES-era colors, crisp pixels,
no text, no UI
```

---

## 3. 對話立繪（路德／瑪琳／亞倫）

> 規格：**正方形 1:1**（生成 1024x1024 即可，我會縮到遊戲用的 144x144）。
> 三張要風格一致：Midjourney 用同一張當 `--sref`；GPT-4o/DALL-E 在同一對話串連續生成。
> 生好後放到 `projects/crystal-quest/design/faces/`（檔名 ludo.png / marin.png / aaron.png），
> 跟我說一聲，我會縮圖、（需要的話）去背，接進對話框與選單，取代現在的程式繪版本。

### 共用風格前綴（每張都加在最前面）

```
16-bit SNES JRPG dialogue portrait, pixel art bust shot, head and shoulders,
facing slightly left, limited color palette, clean pixel outlines, soft two-tone shading,
plain dark navy background, no text, no watermark, no frame
```

### 3-A 路德（男主角・15歲・探索者）

```
a 15-year-old adventurer boy, dark chestnut brown messy short hair, warm amber eyes,
cream long-sleeved shirt under a brown leather chest armor, small rust-red cape
clasped on his shoulders, leather bracers, cheerful confident grin, youthful spark,
protagonist of a fantasy RPG
```

### 3-B 瑪琳（女主角・15歲・探索者）

```
a 15-year-old adventurer girl, auburn red-brown hair in a high ponytail with side bangs,
bright green eyes, white blouse with a deep blue collar, leather bracers,
calm composed smile with a hint of exasperation, dependable childhood friend,
heroine of a fantasy RPG
```

### 3-C 亞倫（導師・A級冒險者・30代後半）

```
a battle-worn male adventurer in his late thirties, short black weathered hair with
grey streaks at the temples, light stubble, a thin old scar on his right cheek,
steel-blue eyes, dark grey heavy armor with metal pauldrons, stern but reliable
expression, veteran mentor of a fantasy RPG
```

---

## 備忘

- 七大陸對應（現行提案）：芙瑞達=人族起點、比爾=矮人、亞力士=翼人、裘恩=精靈、魏恩=獸人、傑魯得=森人、郝麗=妖精。
- 封印地初期無人知曉——世界地圖上**不要**畫任何「中央特殊島嶼」。
- 生成後把喜歡的成品存到 `projects/crystal-quest/design/`，跟 Claude 說一聲即可拿來當美術基準。
