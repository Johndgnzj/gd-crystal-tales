#!/usr/bin/env bash
#
# GDevelop + gdevelop-mcp 一鍵安裝腳本 (macOS)
# 用法：
#   cd 到本檔所在的 GDevelop 資料夾，執行：
#       ./install.sh
#   若權限不足：
#       bash install.sh
#
# 這支腳本會自動：
#   1. 檢查/安裝 Node.js (18+)
#   2. 啟用 pnpm (透過 corepack)
#   3. 下載並建置 gdevelop-mcp
#   4. 自動把 .mcp.json 指向正確路徑
#   5. 檢查 GDevelop 桌面版 與 Claude Code 是否已安裝（未裝只提示，不中斷）
#
set -euo pipefail

# ---------- 樣式 ----------
BOLD=$'\033[1m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; RESET=$'\033[0m'
info(){ printf '%s\n' "${BOLD}▶ $*${RESET}"; }
ok(){   printf '%s\n' "${GREEN}✔ $*${RESET}"; }
warn(){ printf '%s\n' "${YELLOW}⚠ $*${RESET}"; }
err(){  printf '%s\n' "${RED}✖ $*${RESET}" 1>&2; }

# ---------- 定位腳本所在資料夾 ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
MCP_DIR="$SCRIPT_DIR/gdevelop-mcp"
DIST="$MCP_DIR/dist/index.js"

echo
info "GDevelop AI 環境安裝"
printf '  安裝位置：%s\n\n' "$SCRIPT_DIR"

# ---------- 0. 依 .nvmrc 切換 Node 版本 ----------
# 本資料夾有 .nvmrc (=22)，若已裝 nvm 就先切到指定版本，避免用到過舊的預設 Node。
if [ -s "$HOME/.nvm/nvm.sh" ]; then
  export NVM_DIR="$HOME/.nvm"
  # shellcheck disable=SC1090
  . "$HOME/.nvm/nvm.sh"
  nvm use >/dev/null 2>&1 || true
fi

# ---------- 1. Node.js ----------
# pnpm 11.1.2（本專案 packageManager 鎖定版）需要 node:sqlite，僅存在於 Node 22.5+，
# 故此處要求 Node 22 以上（與專案 .nvmrc 一致）。
need_node(){
  if command -v node >/dev/null 2>&1; then
    major="$(node -v | sed 's/^v//' | cut -d. -f1)"
    if [ "${major:-0}" -ge 22 ] 2>/dev/null; then ok "Node.js $(node -v)"; return 0; fi
    warn "Node.js 版本過舊 ($(node -v))，需要 22 以上（pnpm 11 需 node:sqlite）"
  else
    warn "未偵測到 Node.js"
  fi
  return 1
}

install_node(){
  # 已有 nvm（或使用者本來就用 nvm）→ 直接裝 Node 22
  if [ -s "$HOME/.nvm/nvm.sh" ] || command -v nvm >/dev/null 2>&1; then
    export NVM_DIR="$HOME/.nvm"
    # shellcheck disable=SC1090
    . "$HOME/.nvm/nvm.sh" 2>/dev/null || true
    info "以 nvm 安裝 Node.js 22 ..."
    nvm install 22 && nvm use 22
  elif command -v brew >/dev/null 2>&1; then
    info "以 Homebrew 安裝 Node.js 22 ..."
    brew install node@22 || brew install node
    brew link --overwrite --force node@22 2>/dev/null || true
  else
    info "安裝 nvm 並安裝 Node.js 22 ..."
    export NVM_DIR="$HOME/.nvm"
    if [ ! -s "$NVM_DIR/nvm.sh" ]; then
      curl -fsSL -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
    fi
    # shellcheck disable=SC1090
    . "$NVM_DIR/nvm.sh"
    nvm install 22 && nvm use 22
  fi
}

if ! need_node; then
  install_node
  # 若是用 nvm 安裝，載入到目前 shell
  if [ -s "$HOME/.nvm/nvm.sh" ]; then export NVM_DIR="$HOME/.nvm"; . "$HOME/.nvm/nvm.sh"; fi
  need_node || { err "Node 安裝失敗，請手動到 https://nodejs.org 安裝 LTS 後重跑本腳本"; exit 1; }
fi

# ---------- 2. pnpm (corepack) ----------
# 註：不使用 `corepack prepare pnpm@latest`，因為舊版 corepack 會因簽章金鑰過期而
#     報錯 "Cannot find matching keyid"。改為先「更新 corepack」修正金鑰，再由專案
#     package.json 的 packageManager 欄位 (pnpm@11.1.2) 自動決定要用的 pnpm 版本。
info "準備 pnpm（更新 corepack 以修正簽章金鑰問題）..."
npm install -g corepack@latest >/dev/null 2>&1 || warn "corepack 更新略過（沿用現有版本）"
corepack enable 2>/dev/null || sudo corepack enable 2>/dev/null || true
if command -v pnpm >/dev/null 2>&1 || command -v corepack >/dev/null 2>&1; then
  ok "pnpm / corepack 就緒"
else
  err "無法啟用 pnpm，請手動執行：npm install -g corepack@latest && corepack enable"
  exit 1
fi

# ---------- 3. git ----------
if ! command -v git >/dev/null 2>&1; then
  err "找不到 git，請先安裝：xcode-select --install （或到 https://git-scm.com/download/mac）"
  exit 1
fi
ok "git $(git --version | awk '{print $3}')"

# ---------- 4. 下載 / 更新 gdevelop-mcp ----------
if [ -d "$MCP_DIR/.git" ]; then
  info "更新 gdevelop-mcp ..."
  git -C "$MCP_DIR" pull --ff-only || warn "git pull 略過（可能有本機修改），沿用現有版本"
else
  info "下載 gdevelop-mcp ..."
  git clone https://github.com/gb2b/gdevelop-mcp "$MCP_DIR"
fi

# ---------- 5. 安裝依賴 + 建置 ----------
info "安裝依賴（第一次會下載 Chromium，約 170MB，請耐心等）..."
if ! ( cd "$MCP_DIR" && pnpm install ); then
  warn "pnpm install 失敗，改用 COREPACK_INTEGRITY_KEYS=0 重試（略過簽章驗證）..."
  ( cd "$MCP_DIR" && COREPACK_INTEGRITY_KEYS=0 pnpm install )
fi
info "建置 gdevelop-mcp ..."
( cd "$MCP_DIR" && pnpm build )

if [ ! -f "$DIST" ]; then
  err "建置後找不到 $DIST，請看上方訊息排錯"
  exit 1
fi
ok "建置完成：$DIST"

# ---------- 6. 產生/更新 .mcp.json ----------
info "寫入 .mcp.json（自動指向本機路徑）..."
cat > "$SCRIPT_DIR/.mcp.json" <<JSON
{
  "mcpServers": {
    "gdevelop": {
      "command": "node",
      "args": ["$DIST"]
    }
  }
}
JSON
ok ".mcp.json 已指向 $DIST"

# ---------- 7. 其他工具檢查（不中斷）----------
echo
info "其他必要工具檢查："
if [ -d "/Applications/GDevelop.app" ]; then
  ok "GDevelop 桌面版 已安裝"
else
  warn "未偵測到 GDevelop 桌面版 → 請下載安裝：https://gdevelop.io/download"
fi
if command -v claude >/dev/null 2>&1; then
  ok "Claude Code 已安裝"
else
  warn "未偵測到 Claude Code → 安裝說明：https://docs.claude.com/claude-code"
fi

# ---------- 完成 ----------
cat <<DONE

${GREEN}${BOLD}✅ MCP 環境安裝完成！${RESET}

接下來：
  1. cd "$SCRIPT_DIR"
  2. claude                       # 啟動 AI 代理，出現提示時「允許」gdevelop 伺服器
  3. 在對話中先執行： sync_gdevelop_sources()  接著 gdevelop_overview()
  4. 請 AI 開啟 projects/my-first-game/game.json 開始做遊戲

  （若 GDevelop 桌面版尚未安裝，請先完成上面的下載連結）
DONE
