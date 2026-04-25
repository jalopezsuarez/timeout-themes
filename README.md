# timeout-themes

Custom themes for [Dejal Time Out](https://dejal.com/timeout/) **3.0 (3008)**.

Time Out is a macOS break reminder app. A *theme* is a `.totheme` bundle that Time Out displays during a break — internally it's a folder with an `Info.json` and a `Documents/` web payload (HTML + JS + assets) rendered in a WebView.

## Themes in this repo

### AppleWallpapers.totheme

Random fullscreen slideshow of Apple's stock macOS wallpapers. Each image fades into the next every 15 seconds. The queue is shuffled so no image repeats until all have been shown.

## Bundle layout

```
AppleWallpapers.totheme/
├── Info.json              # Theme metadata (name, version, author, identifier)
└── Documents/
    ├── index.html         # Entry point (rootDocument in Info.json)
    ├── manifest.js        # Generated list of image filenames
    ├── manifest.py        # Indexer — regenerates manifest.js from images/
    └── images/            # Wallpaper files (.jpg, .png, .heic, ...)
```

### `Info.json`

Theme metadata read by Time Out:

| Field          | Purpose                                                         |
| -------------- | --------------------------------------------------------------- |
| `name`         | Display name in Time Out's theme picker                         |
| `identifier`   | Reverse-DNS unique ID                                           |
| `version`      | Bump on every change so Time Out reloads the bundle             |
| `rootDocument` | HTML file loaded in the WebView (`index.html`)                  |
| `author`       | Name / email / url shown in theme info                          |
| `credits`      | Upstream attribution                                            |
| `comments`     | Short description                                               |
| `created` / `modified` | ISO dates                                               |

### `index.html`

Self-contained slideshow. Two stacked `<div>` layers crossfade between images via CSS `opacity` transitions. Key constants:

- `CHANGE_INTERVAL_MS` — time between transitions (currently `0.25 * 60 * 1000` = 15 s; set to `5 * 60 * 1000` for the typical 5-minute break)
- `IMAGE_DIRECTORY` — `images/` (relative to `index.html`)

Image source resolution (in order):
1. **Directory listing** — tries `fetch("images/")`. Works if served by an HTTP server that returns an autoindex page (`python3 -m http.server`); fails silently inside Time Out's WebView and on `file://`.
2. **Manifest fallback** — uses `window.TIMEOUT_WALLPAPER_IMAGES` from `manifest.js`. **This is the path Time Out actually uses.**

Persistence: shuffled queue + last shown image are saved in `sessionStorage`, so reloading the page resumes the cycle. Closing the window or regenerating `manifest.js` resets it (the storage key includes the full image list).

### `manifest.js`

Plain JS that sets one global:

```js
window.TIMEOUT_WALLPAPER_IMAGES = [
  "Big Sur Aerial.heic",
  "Flower 1.jpg",
  ...
];
```

`index.html` reads this list and prepends `images/` to each filename.

### `manifest.py`

Tiny indexer. Run it any time you add/remove files in `images/`:

```bash
cd AppleWallpapers.totheme/Documents
python3 manifest.py
```

It scans `images/` for `.jpg`, `.jpeg`, `.png`, `.heic`, `.webp`, `.gif` and rewrites `manifest.js` with the sorted list. No dependencies — stdlib only.

## Installing a theme in Time Out 3.0 (3008)

1. Run `python3 manifest.py` to make sure `manifest.js` reflects what's in `images/`.
2. Bump `version` in `Info.json` (Time Out caches by version).
3. Double-click the `.totheme` folder, or in Time Out: **Preferences → Themes → +** and pick the bundle.
4. Assign it to a break (Normal / Micro) and trigger a break to verify.

## Previewing in a browser

Open `Documents/index.html` directly:

```bash
open -a Safari AppleWallpapers.totheme/Documents/index.html
```

Notes:
- **Use Safari.** Chrome/Firefox don't render `.heic` → black screen if your manifest is HEIC-only.
- On `file://` the directory-listing fetch is blocked by CORS (harmless — the script falls back to `manifest.js`).
- For a Chrome-friendly preview with autoindex, serve over HTTP: `python3 -m http.server 8000` from `Documents/` and open `http://localhost:8000/`.

## Adding your own wallpapers

```bash
cp /path/to/your/*.jpg AppleWallpapers.totheme/Documents/images/
cd AppleWallpapers.totheme/Documents
python3 manifest.py
```

Then bump `Info.json#version` and reinstall the theme in Time Out.

## Credits

- [Dejal Time Out](https://dejal.com/timeout/) — the host app.
- Apple — original wallpaper assets.
