# Coinness Discord News Bot

[한국어](README.md) · [日本語](README.ja.md) · **English**

A simple bot that pulls cryptocurrency news in real time from the Coinness API and posts it to Discord.

## 🚀 Features

- 📰 Detects new articles automatically every 10 seconds
- 🔥 Distinguishes breaking news from ordinary news
- 📊 Shows market reaction (bullish/bearish votes)
- 🎨 Clean messages using Discord embeds
- 💾 Deduplication by file comparison

## 📋 Requirements

- Python 3.8+
- A Discord bot token
- An internet connection

## 🛠️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root with:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
COINNESS_API_URL=https://api.coinness.com/feed/v1/breaking-news
```

> **Notes**
> - `DISCORD_BOT_TOKEN` is **required**. Without it the bot prints a message and exits instead of starting.
> - `COINNESS_API_URL` is the news API endpoint, read in code via `os.getenv('COINNESS_API_URL')`.
> - `.env` is listed in `.gitignore` and is never committed.

## 🤖 Creating a Discord bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Enter a bot name and click "Create"
4. Click "Bot" in the left menu
5. Click "Add Bot"
6. In the "Token" section click "Copy"
7. Paste the token into your `.env`

## 🎯 Choosing the notification channel

1. Pick the channel that should receive news
2. Open its settings (gear icon)
3. On the "Overview" tab, set the channel topic to `coin_news`
4. Save

## 🚀 Running the bot

```bash
python discord_bot.py
```

On a successful start you'll see something like:

```
코인니스 뉴스 봇#1234이(가) 로그인했습니다!
Bot ID: 123456789012345678
뉴스 알림 대상: 채널 주제가 "coin_news"인 모든 채널
------
발견된 대상 채널: 2개
  - #crypto-news (서버: My Server)
  - #coin-updates (서버: Trading Guild)
------
```

## 🔄 Automatic behavior

- **Polling**: checks for new articles every 10 seconds
- **Live alerts**: posts automatically whenever something new appears
- **Deduplication**: file comparison excludes already-sent articles
- **Breaking news**: shown in red, with an @everyone mention and pinned
- **Multi-channel**: posts to every channel whose topic is "coin_news"

## 📁 File layout

```
crypto_news_bot/
├── discord_bot.py      # main bot (10s news polling, channel discovery, embed sending)
├── coinness_api.py     # Coinness API client (async via aiohttp)
├── requirements.txt    # dependencies
├── .env               # environment variables (create it yourself; gitignored)
├── last_news.json     # previous news snapshot (used for dedup)
└── README.md          # this file
```

## ⚠️ Cautions

- Never share your Discord bot token
- Keep `.env` in `.gitignore`
- Make sure the bot has permission to send messages

## 🐛 Troubleshooting

### The bot doesn't respond

1. Check the bot token is correct
2. Check the bot has been invited to the server
3. Check it has read/send message permissions
4. Check the channel topic is set to "coin_news"

### API errors

1. Check your internet connection
2. Check the Coinness API server status
3. Retry after a while

## 📊 API details

- **Data source**: [Coinness](https://coinness.com)
- **Endpoint**: `https://api.coinness.com/feed/v1/breaking-news`
- **Language**: Korean (ko)
- **Poll interval**: every 10 seconds

## 🤝 Contributing

Bug reports and feature suggestions are always welcome!

## 📄 License

Released under the MIT License.

---

## 👤 Contribution & development environment

| Item | Detail |
|---|---|
| **Contribution share** | **100%** (solo development) |
| **Commits** | 4 / 4 (mine / all human commits) |
| **Contributors** | 1 |

<sub>Counting basis: commits reachable from **every branch** on origin (merge commits and empty commits excluded), counted by commit author email with one person’s multiple addresses merged; bot and automation commits are excluded.</sub>
