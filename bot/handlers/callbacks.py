import os
from telegram import Update
from telegram.ext import ContextTypes
from services.youtube_service import download_youtube_audio, download_youtube_video


async def format_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    action, url = data.split(":", 1)

    msg = await query.edit_message_text("⏳ Downloading...")

    try:
        if action == "audio":
            filepath = await download_youtube_audio(url)
            await query.message.reply_audio(audio=open(filepath, "rb"))
            os.remove(filepath)

        elif action == "video":
            filepath = await download_youtube_video(url)
            await query.message.reply_video(video=open(filepath, "rb"))
            os.remove(filepath)

        await msg.delete()

    except ValueError as e:
        await query.edit_message_text(f"❌ Error: {e}")


async def quality_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    _, quality, url = data.split(":", 2)

    await query.edit_message_text(f"⏳ Downloading {quality}p video...")

    try:
        filepath = await download_youtube_video(url, quality=quality)
        await query.message.reply_video(video=open(filepath, "rb"))
        os.remove(filepath)
        await query.message.delete()
    except ValueError as e:
        await query.edit_message_text(f"❌ Error: {e}")


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ Cancelled.")
