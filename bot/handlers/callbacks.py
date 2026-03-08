import os
from telegram import Update
from telegram.ext import ContextTypes
from services.media_service import download_video, download_audio

MAX_SIZE_BYTES = 50 * 1024 * 1024


def _check_size(filepath: str) -> bool:
    return os.path.getsize(filepath) <= MAX_SIZE_BYTES


async def format_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    action, url_id = query.data.split(":", 1)
    url = context.user_data.get(url_id)

    if not url:
        await query.edit_message_text("Session expired. Please send the URL again.")
        return

    msg = await query.edit_message_text("Downloading...")

    filepath = None
    try:
        if action == "audio":
            filepath = await download_audio(url)
            if not _check_size(filepath):
                await query.edit_message_text("File exceeds Telegram's 50MB limit.")
                return
            await query.message.reply_audio(audio=open(filepath, "rb"))

        elif action == "video":
            filepath = await download_video(url)
            if not _check_size(filepath):
                await query.edit_message_text("File exceeds Telegram's 50MB limit.")
                return
            await query.message.reply_video(video=open(filepath, "rb"))

        await msg.delete()

    except ValueError as e:
        await query.edit_message_text(f"Error: {e}")

    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


async def quality_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    _, quality, url_id = query.data.split(":", 2)
    url = context.user_data.get(url_id)

    if not url:
        await query.edit_message_text("Session expired. Please send the URL again.")
        return

    await query.edit_message_text(f"Downloading {quality}p video...")

    filepath = None
    try:
        filepath = await download_video(url, quality=quality)
        if not _check_size(filepath):
            await query.edit_message_text("File exceeds Telegram's 50MB limit.")
            return
        await query.message.reply_video(video=open(filepath, "rb"))
        await query.message.delete()

    except ValueError as e:
        await query.edit_message_text(f"Error: {e}")

    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Cancelled.")