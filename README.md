# Yandex.Music Downloader

Asynchronous downloader for favorite tracks from Yandex.Music.

## Installation

```bash
git clone https://github.com/chuhan3131/YMD-of-favorite-tracks.git
cd YMD-of-favorite-tracks
pip install -r requirements.txt
```

## Usage

```bash
python main.py --token "y0__xxxxxxxxxxxxxxx-xxxxxxxxxxxx_xxxxxxxx-xxxxxxxxxxx-xx"

# With custom directory
python main.py --token "y0__xxxxxxxxxxxxxxx-xxxxxxxxxxxx_xxxxxxxx-xxxxxxxxxxx-xx" --directory "Music"
```

## Arguments

- `-t, --token` - Yandex.Music token (**required**)
- `-d, --directory` - Download folder (default: `downloads`)

## Getting Token

1. Open Yandex.Music in your browser
2. Press F12 → Application tab → Local Storage
3. Find the `access_token` or `token` key
4. Copy the token value

## Project Structure

```
YMD-of-favorite-tracks/
├── main.py          # Main script
├── downloader.py    # Download logic
├── logger.py        # Color logging
└── requirements.txt # Dependencies
```

## Features

- Download your favorite tracks from Yandex.Music
- Asynchronous processing 
- Customizable download directory
- Colored console logging

---
## Blog [chuhandev.t.me](https://t.me/chuhandev)
**Note:** Not an official project
