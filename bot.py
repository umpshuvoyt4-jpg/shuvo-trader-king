
import os, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from signal_engine import get_signal

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SYMBOLS = [x.strip().upper() for x in os.getenv("SYMBOLS", "BTCUSDT,ETHUSDT").split(",")]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Signal Board.\\n/signals - latest signals\\n"
        "/signal BTCUSDT - one market\\n/subscribe - automatic updates every minute\\n"
        "/unsubscribe - stop automatic updates"
    )

async def build_report(symbols):
    lines = ["📊 SIGNAL BOARD — 1m", "Data: Binance public spot (not Quotex quotes)", ""]
    for symbol in symbols:
        try:
            s = await asyncio.to_thread(get_signal, symbol)
            emoji = "🟢" if s["direction"] == "UP" else "🔴" if s["direction"] == "DOWN" else "⚪"
            lines.append(f"{emoji} {s['symbol']}: {s['direction']} | RSI {s['rsi']} | Price {s['price']}")
            lines.append(s["reason"])
        except Exception as exc:
            lines.append(f"⚠️ {symbol}: data unavailable ({exc})")
    lines.append("\\nEducational demo only. No guaranteed results.")
    return "\\n".join(lines)

async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(await build_report(SYMBOLS))

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = context.args[0].upper() if context.args else "BTCUSDT"
    await update.message.reply_text(await build_report([symbol]))

async def push_updates(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    await context.bot.send_message(chat_id=chat_id, text=await build_report(SYMBOLS))

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if context.job_queue.get_jobs_by_name(str(chat_id)):
        await update.message.reply_text("Automatic updates are already enabled.")
        return
    context.job_queue.run_repeating(push_updates, interval=60, first=2,
                                    chat_id=chat_id, name=str(chat_id))
    await update.message.reply_text("Automatic signal updates enabled: every 60 seconds. Use /unsubscribe to stop.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("Automatic updates stopped.")

def main():
    if not TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN in .env first")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signals", signals))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.run_polling()

if __name__ == "__main__":
    main()
