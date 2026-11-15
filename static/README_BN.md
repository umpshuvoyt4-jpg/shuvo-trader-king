# Signal Board Starter — Website + Telegram

এটি ভিডিওর মতো dark/neon signal-board UI-সহ একটি **starter project**। এতে একটি সাধারণ EMA/RSI উদাহরণ স্ট্র্যাটেজি আছে।

## গুরুত্বপূর্ণ সীমাবদ্ধতা
- ডেটা আসে Binance-এর public spot candle endpoint থেকে; এটি Quotex-এর নিজস্ব/OTC price feed নয়।
- Quotex-এর জন্য নির্ভুল সিগন্যাল দিতে হলে Quotex-এ দেখা একই instrument-এর নির্ভরযোগ্য অনুমোদিত market-data source দরকার।
- এটি কোনো trade execute করে না, profit বা accuracy guarantee দেয় না। `confidence` এখানে কেবল demo label, backtested probability নয়।
- প্রথমে demo/paper mode-এ পরীক্ষা করুন।

## চালাতে
Python 3.10+ ইনস্টল করে project folder-এ:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` ফাইলে Telegram bot token বসান। Telegram-এ `@BotFather` খুলে `/newbot` দিয়ে bot বানিয়ে token নিন। Token কাউকে দেবেন না, public chat-এ পাঠাবেন না।

### Website
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
তারপর browser-এ `http://127.0.0.1:8000` খুলুন।

### Telegram bot
অন্য terminal-এ একই folder থেকে:
```bash
# .env variables load করুন
# Linux/macOS:
export $(grep -v '^#' .env | xargs)
# Windows PowerShell:
# Get-Content .env | ForEach-Object { if ($_ -match '^([^#][^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1],$matches[2]) } }
python bot.py
```
Telegram bot-এ `/start`, `/signals`, বা `/signal BTCUSDT` লিখুন। প্রতি মিনিটে স্বয়ংক্রিয় আপডেট পেতে `/subscribe` এবং বন্ধ করতে `/unsubscribe` লিখুন।

## Pair বদলানো
`.env`-এ `SYMBOLS=BTCUSDT,ETHUSDT` বদলান। এখানে Binance-এ থাকা symbol ব্যবহার করতে হবে।

## পরের ধাপ
Quotex-এর নির্দিষ্ট pair, timeframe, এবং একই market-এর trusted data source নিশ্চিত হলে adapter ও strategy সেটি অনুযায়ী বদলাতে হবে। Telegram group/channel-এ সিগন্যাল পাঠানোর আগে bot-কে সেখানে যোগ করে প্রয়োজনীয় permission দিতে হবে।
