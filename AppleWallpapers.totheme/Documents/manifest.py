import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "images")
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp", ".gif")

files = sorted(f for f in os.listdir(IMAGES) if f.lower().endswith(EXTS))
lines = ",\n".join("  " + json.dumps(f) for f in files)

with open(os.path.join(HERE, "manifest.js"), "w") as fh:
    fh.write("window.TIMEOUT_WALLPAPER_IMAGES = [\n" + lines + "\n];\n")

print(f"{len(files)} images")
