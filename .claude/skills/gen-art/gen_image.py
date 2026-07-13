#!/usr/bin/env python3
"""Gemini 產圖腳本（gen-art skill 的執行端）。

用法：
  python3 gen_image.py --type face     --prompt "鐵匠漢克：壯碩中年男子、絡腮鬍、皮圍裙" --out design/faces/Hank.png
  python3 gen_image.py --type battlebg --prompt "廢棄礦坑深處，藍黑色調"                --out assets/ui/battlebg_cave2.png
  python3 gen_image.py --type raw      --prompt "..." --ar 1:1 --out /tmp/test.png

金鑰：讀環境變數 GEMINI_API_KEY，否則往上層目錄找 .env（KEY=VALUE 格式）。
模型：gemini-2.5-flash-image（失敗時退 gemini-2.0-flash-preview-image-generation）。
"""
import argparse, base64, json, os, sys, time, urllib.request, urllib.error

MODELS = ["gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"]

# 各素材類型的風格前綴（維持與遊戲現有素材一致的構圖約定）
STYLES = {
    # John 的立繪管線約定：橫幅、人物偏左、右側裝飾星、深藍底 → art_v7_faces.py 自動裁 144px 頭像
    "face": ("Anime fantasy RPG character portrait banner, clean cel-shaded illustration "
             "(smooth painted style, NOT pixel art). The character occupies the LEFT third "
             "of the frame, bust-up view, facing slightly right, warm key light. Solid very "
             "dark navy blue background, a few small decorative star sparkles on the right "
             "side. Absolutely no text, no letters, no numbers, no watermark. Character: "),
    "battlebg": ("Side-view JRPG battle background, painterly pixel-art style, rich vivid colors, "
                 "clearly lit and readable (NOT dark, NOT black), gentle depth, empty flat middle "
                 "ground for combatants to stand on, horizon around upper third, "
                 "no characters, no people, no text, no UI. Scene: "),
    "map": ("Hand-drawn fantasy region map, parchment-free dark style, bird's-eye view, clear "
            "landmarks and roads, Traditional Chinese label-free (no text at all). Region: "),
    "title": ("Fantasy JRPG title screen key art, dramatic sky, no logo, no text, cinematic "
              "lighting. Scene: "),
    "icon": ("Single game icon, centered subject, dark background, clean silhouette, no text. "
             "Subject: "),
    # 45° 斜角像素建築外觀（洋紅底去背 → 縮放置放於地圖）
    "building": ("Pixel art game asset sprite, 45-degree oblique isometric view, clean readable 2D "
                 "JRPG style matching a classic pixel-art fantasy town, cohesive warm palette, "
                 "centered, on a solid flat magenta #ff00ff background for easy cutout, no ground "
                 "plane, no drop shadow, no text, no letters, no numbers, no people. Building: "),
    # 就地室內大圖（斜角剖面房間，洋紅底去背）
    "interior": ("Pixel art 2D JRPG interior room, 45-degree oblique cutaway view, cozy and "
                 "detailed furniture, warm lantern light, solid flat magenta #ff00ff background "
                 "surrounding the room for easy cutout, no characters, no people, no text, "
                 "no letters. Room: "),
    "raw": "",
}
ASPECT = {"face": "16:9", "battlebg": "16:9", "map": "16:9", "title": "16:9", "icon": "1:1",
          "building": "1:1", "interior": "4:3", "raw": None}


def find_key():
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"].strip()
    d = os.path.abspath(os.path.dirname(__file__))
    for _ in range(8):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    sys.exit("找不到 GEMINI_API_KEY（環境變數或上層 .env）")


def generate(key, model, prompt, aspect):
    gc = {"responseModalities": ["IMAGE"]}
    if aspect:
        gc["imageConfig"] = {"aspectRatio": aspect}
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": gc}).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    for part in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("回應中沒有圖片：" + json.dumps(d)[:300])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", default="raw", choices=list(STYLES))
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ar", default=None, help="覆寫長寬比，如 16:9 / 1:1 / 3:4")
    a = ap.parse_args()

    key = find_key()
    prompt = STYLES[a.type] + a.prompt
    aspect = a.ar or ASPECT[a.type]
    last = None
    for model in MODELS:
        for attempt in range(3):
            try:
                png = generate(key, model, prompt, aspect)
                os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
                open(a.out, "wb").write(png)
                print(f"OK {a.out} ({len(png)} bytes, model={model})")
                return
            except urllib.error.HTTPError as e:
                last = f"{model} HTTP {e.code}: {e.read()[:200]}"
                if e.code in (429, 500, 503):
                    time.sleep(3 * (attempt + 1)); continue
                break
            except Exception as e:
                last = f"{model}: {e}"
                time.sleep(2)
    sys.exit("生成失敗：" + str(last))


if __name__ == "__main__":
    main()
