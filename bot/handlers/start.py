from telegram import Update
from telegram.ext import ContextTypes

START_TEXT = """
👋 *Welcome to MediaGram Bot*

I can download videos and audio from multiple platforms directly to your Telegram chat

*📥 Supported Platforms:*
• ▶️ YouTube
• 🎵 TikTok
• 📸 Instagram
• 📘 Facebook

*⚡ How to use:*
Just paste any supported URL and I'll do the rest

*📋 Commands:*
• `/start` — Show this menu
• `/help` — How to use the bot
"""

HELP_TEXT = """
*How to use MediaGram Bot:*

*Step 1:* Paste a link from YouTube, TikTok, Instagram or Facebook
*Step 2:* Pick your format from the buttons:
  • 🎵 Audio MP3
  • 🎬 Video MP4
  • 🎬 360p  720p  1080p

*⚠️ Limitations:*
• Files over 50MB can't be sent via Telegram
• Instagram: public posts only
• Facebook: public videos only
• TikTok: no watermark when possible
"""


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 *Welcome, {user.first_name}*\n" + START_TEXT,
        parse_mode="MarkdownV2"
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="MarkdownV2")