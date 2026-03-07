from telegram import Update
from telegram.ext import ContextTypes

START_TEXT = """
👋 *Welcome to YTGram Bot*

I can download YouTube videos and audio directly to your Telegram chat

*📥 What I can do:*
• `/audio <url>` — Download as MP3
• `/video <url>` — Download as MP4
• `/start` — Show this menu
• `/help` — How to use the bot


_Just paste any YouTube URL and I'll do the rest!_ 🎯
"""

HELP_TEXT = """
*📖 How to use YTGram Bot:*

*Download Audio (MP3):*
`/audio https://youtube\.com/watch?v=xxxxx`

*Download Video \(MP4\):*
`/video https://youtube\.com/watch?v=xxxxx`

*Or just paste a YouTube URL* and pick a format from the buttons

*Supported URLs:*
• Standard YouTube links
• YouTube Shorts
• youtu\.be short links

*⚠️ Limitations:*
• Max video length: 60 minutes
• Files over 50MB can't be sent via Telegram
"""


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"*Welcome, {user.first_name}*\n" + START_TEXT,
        parse_mode="MarkdownV2"
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="MarkdownV2")
