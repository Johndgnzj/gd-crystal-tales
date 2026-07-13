# 素材授權標註

## 角色圖（Universal LPC Spritesheet Generator）
本專案 4 名角色由 [LPC 角色產生器](https://github.com/liberatedpixelcup/Universal-LPC-Spritesheet-Character-Generator) 的圖層合成（部分圖層經程式染色）：

| 角色 | 使用圖層 |
|------|----------|
| 亞倫（主角） | `body/bodies/male`、`head/heads/human/male`、`legs/pants/male`、`feet/boots/rimmed/male`、`torso/clothes/longsleeve/longsleeve/male`、`hair/bedhead/adult` |
| 村長 | `body/bodies/male`、`head/heads/human/male_elderly`、`legs/pants/male`、`feet/shoes/basic/male`、`torso/clothes/longsleeve/longsleeve/male`、`hair/balding/adult`、`beards/beard/winter/male` |
| 米拉（村婦） | `body/bodies/female`、`head/heads/human/female`、`legs/skirts/plain/thin`、`feet/shoes/basic/thin`、`torso/clothes/shortsleeve/shortsleeve/female`、`hair/braid/adult/bg+fg` |
| 衛兵 | `body/bodies/male`、`head/heads/human/male`、`legs/pants/male`、`feet/boots/rimmed/male`、`torso/chainmail/male`、`hat/helmet/bascinet/adult` |

> ⚠️ **重要**：LPC 素材採混合授權（CC-BY-SA 3.0 / GPL 3.0 / CC0 / OGA-BY 等），**發佈遊戲前必須標註每個圖層的原作者**。
> 完整的作者/授權對照在 `tools/lpc/CREDITS.csv`，或用 LPC 網頁工具（liberatedpixelcup.github.io）產生角色時直接下載對應的 credits 檔。
> 目前這只是內部 demo，尚未做完整逐項標註——正式上架前要補齊。

## 地圖
- 瓦片圖（`assets/map/atlas.png`）與地圖（`assets/map/world.tmj`）為本專案用程式生成，可自由使用。
- 地圖用 [Tiled](https://www.mapeditor.org/)（GPL/免費）編輯，格式為 Tiled JSON（.tmj），GDevelop 桌面版原生支援匯入。
