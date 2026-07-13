# GDevelop + AI 代理 環境（從零安裝與使用）

> 建立日期：2026-07-10
> 目標：在你的 Mac 上把 **GDevelop（免費遊戲引擎）** 和 **gdevelop-mcp（讓 AI 代理直接做遊戲）** 都準備好，並附一個已經建好的起始專案。

---

## 這個資料夾裡有什麼

```
GDevelop/
├── README_安裝與使用.md          ← 你正在看的這份
├── .mcp.json                     ← AI 代理(MCP)設定檔，已幫你填好路徑
├── .gitignore
├── projects/
│   └── my-first-game/
│       └── game.json             ← 已建好的起始專案（platformer，1280×720）
├── assets/                       ← 放你自己的美術/音效素材
├── builds/                       ← HTML5 匯出成品放這
├── docs/                         ← 筆記
└── gdevelop-mcp/                 ← 待你 clone（見 Step 3）
```

> `game.json` 是合法的 GDevelop 專案，內含 `Level1` 場景、`Player`（含平台跳躍行為）、`Ground`（平台）。目前沒有貼圖，之後由你或 AI 代理加素材即可。

---

## 一鍵安裝（推薦）

大部分步驟已寫成腳本 `install.sh`。打開「終端機（Terminal）」執行：

```bash
cd "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop"
./install.sh          # 若權限不足改用： bash install.sh
```

腳本會自動：檢查/安裝 **Node.js** → 啟用 **pnpm** → 下載並建置 **gdevelop-mcp** → 把 `.mcp.json` 指到正確路徑 → 檢查 GDevelop 桌面版與 Claude Code 是否已裝。

> ⚠️ 腳本**不會**自動安裝 GDevelop 桌面版與 Claude Code（這兩個是 GUI 程式）。若尚未安裝，依腳本結尾提示的連結手動裝即可（見下方 Step 1、Step 4）。
> 想自己一步步做、或安裝卡關時，往下看完整手動步驟。

---

## 安裝總覽（四步，手動）

1. 裝 **GDevelop 桌面版**（做遊戲、預覽、匯出用）
2. 裝 **Node.js 18+** 並啟用 **pnpm**（跑 MCP 用）
3. 取得並建置 **gdevelop-mcp**
4. 在 **AI 代理（Claude Code）** 掛上 MCP，開始用 AI 做遊戲

全部免費。以下指令都在「終端機（Terminal）」執行。

---

## Step 1 — 安裝 GDevelop 桌面版

1. 到官網下載：https://gdevelop.io/download
2. 下載 macOS 版，安裝後打開一次確認能開。
3. 之後要開起始專案：GDevelop →「開啟專案」→ 選
   `…/GameCreator/GDevelop/projects/my-first-game/game.json`

---

## Step 2 — 安裝 Node.js 與 pnpm

**2-1 裝 Node.js（需 22 以上）**

> ⚠️ 本專案鎖定 pnpm 11，需要 **Node 22+**（Node 20 以下會出現 `node:sqlite` 錯誤）。

用 nvm（推薦，可切換版本）：

```bash
nvm install 22
nvm use 22
```

或到 https://nodejs.org 下載 **22 以上**的安裝包。裝完確認：

```bash
node --version   # 需顯示 v22 以上
```

> 📌 本資料夾已放 `.nvmrc`（內容 `22`）。往後在這個資料夾只要執行 `nvm use`，就會自動切到 Node 22；`install.sh` 開頭也會自動依它切換。
> 想每次 `cd` 進來就自動切版本，可在 `~/.zshrc` 加上 nvm 的 auto-use 掛勾（我可以幫你加）。
> 想讓所有新終端機都預設 22：`nvm alias default 22`。

**2-2 啟用 pnpm（Node 內建的 Corepack 就能開）**

```bash
corepack enable
corepack prepare pnpm@latest --activate
pnpm --version   # 顯示版本號即成功（需 11 以上）
```

---

## Step 3 — 取得並建置 gdevelop-mcp

把它 clone 到**這個資料夾底下**（路徑要和 `.mcp.json` 一致）：

```bash
cd "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop"
git clone https://github.com/gb2b/gdevelop-mcp
cd gdevelop-mcp
pnpm install     # 第一次會下載 Chromium（約 170MB），請耐心等
pnpm build       # 產生 dist/index.js
```

完成後應該存在這個檔：
`…/GameCreator/GDevelop/gdevelop-mcp/dist/index.js`
（`.mcp.json` 已經指向它，不用改。）

> 沒有 git？到 https://git-scm.com/download/mac 安裝，或先用 `xcode-select --install`。

---

## Step 4 — 在 AI 代理掛上 MCP

本環境用 **Claude Code**（免費/付費皆可）作為 AI 代理。

1. 安裝 Claude Code：https://docs.claude.com/claude-code （依官網指示）
2. 在終端機進入這個資料夾再啟動：

   ```bash
   cd "/Users/john/Projects/60_soho/30_Personal/GameCreator/GDevelop"
   claude
   ```

3. Claude Code 會偵測到本資料夾的 `.mcp.json`，詢問是否啟用 `gdevelop` 伺服器 → **允許**。
4. 成功後，工具會以 `mcp__gdevelop__*` 出現（共 30 個工具）。

> 也可用 Cursor 等其他支援 MCP 的工具，設定方式類似（指到同一個 `dist/index.js`）。

---

## Step 5 — 第一次啟動要下的指令

在 AI 代理裡，第一次先讓它抓 GDevelop 官方原始碼（只需一次）：

```
請執行 sync_gdevelop_sources()          ← 下載官方原始碼(~14MB)到快取
再執行 gdevelop_overview()               ← 讀架構地圖，之後更省 token
```

然後就能請它動工，例如：

```
用 gdevelop-mcp 開啟我的專案
projects/my-first-game/game.json，
先 inspect_project 看現況，
再幫 Player 從 asset store 找一個 CC0 角色貼圖、
做出左右移動 + 跳躍，並用 preview_scene 給我截圖。
```

---

## Step 6 — 預覽與匯出 HTML5（可商用、發佈 Web）

- **預覽**：在 GDevelop 桌面版按「預覽」▶，或請 AI 用 `preview_scene` 截圖。
- **匯出 Web**：GDevelop →「匯出/發佈」→ 選 **HTML5（本機資料夾）** →
  輸出到 `…/GDevelop/builds/`。可無限次免費匯出，成品可自由上架/販售（引擎為 MIT 授權）。

---

## 常用 AI 提示詞範例

- 「用 `list_examples` 找 platformer 範例，仿它把我的專案做成 3 關。」
- 「用 `search_assets` 找像素風地磚，`import_assets_into_project` 匯入當地板。」
- 「幫 Player 加二段跳；改完先 `dryRun` 給我看 diff 再套用。」
- 「做一個開始畫面場景，有標題與『開始』按鈕，點了進 Level1。」
- 「這個專案哪裡怪怪的？用 `validate_project` 檢查並修好。」

> 安全機制：每次寫入前會先驗證、自動備份，可用 `undo_last_edit` 還原、`diff_projects` 比對。放心讓 AI 改。

---

## 疑難排解

- **`.mcp.json` 沒被偵測**：確認你是「在 GDevelop 這層資料夾」啟動 Claude Code，且 `gdevelop-mcp/dist/index.js` 存在。
- **`pnpm` 找不到**：重跑 `corepack enable`，或關掉終端機重開。
- **corepack 報 `Cannot find matching keyid`**：這是舊版 corepack 簽章金鑰過期的已知 bug。修法：
  ```bash
  npm install -g corepack@latest   # 更新 corepack（關鍵）
  corepack enable
  cd "…/GDevelop/gdevelop-mcp" && pnpm install && pnpm build
  ```
  仍失敗時可暫時略過驗證：`COREPACK_INTEGRITY_KEYS=0 pnpm install`。（`install.sh` 已內建這兩道修正，重跑即可。）
- **報 `No such built-in module: node:sqlite`**：Node 版本太舊。pnpm 11 需要 **Node 22+**。修法：
  ```bash
  nvm install 22 && nvm use 22
  cd "…/GDevelop/gdevelop-mcp" && pnpm install && pnpm build
  ```
- **Chromium 下載失敗/很慢**：重跑 `pnpm install`；`preview_scene`（真實預覽）才需要它，`render_scene_static`（快速靜態圖）不需要。
- **GDevelop 開不了 game.json**：多半是 GDevelop 版本太舊，更新到最新版即可（本專案以 5.6 格式產生）。
- **不想設定 MCP**：GDevelop 桌面版內建付費 AI 助手也能用，但 `gdevelop-mcp` 免費且工具更多。

---

## 參考連結

- GDevelop 官網／下載：https://gdevelop.io/ ／ https://gdevelop.io/download
- gdevelop-mcp（GitHub）：https://github.com/gb2b/gdevelop-mcp
- Node.js：https://nodejs.org ／ Claude Code：https://docs.claude.com/claude-code
