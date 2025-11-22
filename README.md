# Yandex.Music Downloader

Asynchronous downloader for favorite tracks from Yandex.Music.

![ymd](https://github.com/user-attachments/assets/017742f0-2d90-4052-b014-c4315a356e31)



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

**You cannot create your own OAuth application. The only option is to use the official Yandex.Music client applications.**

### Available Methods:

- **[Website](https://music-yandex-bot.ru/)** (may not work for all accounts)
- **[Android APK](https://github.com/MarshalX/yandex-music-token/releases)**
- **[Chrome Extension](https://chrome.google.com/webstore/detail/yandex-music-token/lcbjeookjibfhjjopieifgjnhlegmkib)**
- **[Firefox Extension](https://addons.mozilla.org/en-US/firefox/addon/yandex-music-token/)**

All methods above provide open-source code available [here](https://github.com/MarshalX/yandex-music-token).

### Easiest Method (Browser):

1. Open browser DevTools and enable network throttling in the Network tab
2. Visit: [https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d](https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d)
3. Log in and grant permissions
4. The browser will redirect to a URL like: `https://music.yandex.ru/#access_token=AQAAAAAYc***&token_type=bearer&expires_in=31535645`
5. Copy the token from the `access_token` parameter in the URL

> **Tip:** The redirect happens quickly, so enable network throttling to capture the token.

### Network Throttling Guides:
- [Chrome](https://www.browserstack.com/guide/how-to-perform-network-throttling-in-chrome)
- [Firefox](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/throttling/index.html)

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
- Asynchronous processing for faster downloads
- Customizable download directory
- Colored console logging

---

**Developer Blog:** [chuhandev.t.me](https://t.me/chuhandev)

*Note: This is not an official Yandex project*
