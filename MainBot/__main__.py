from MainBot import (
    LOGGER,
    application,
    LOGGER,
    BOT_USERNAME,
    DEV_USERNAME,
    TOPIC_ID,
    TOPIC_THREADS,
    OWNER_ID,
)
import traceback
import json
from telegram import Update
import html
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import io


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name
    message = update.effective_message

    msg = f"Hey there *{first_name}*!\nThis is @{BOT_USERNAME}\n\nA telegram bot which can help you manage your topic groups with multiple topics.\n\nMade with ❤️ By @{DEV_USERNAME}"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Add To Channel",
                    url=f"https://t.me/{BOT_USERNAME}?startchannel",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Add To Group",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup",
                ),
            ],
        ]
    )
    await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    if "RemoteDisconnected" in context.error.__format__(""):
        return
    LOGGER.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    n = len(message)
    if n > 2000:
        message = (
            "An exception was raised while handling an update\n"
            f"update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}\n\n"
            f"context.chat_data = {html.escape(str(context.chat_data))}\n\n"
            f"context.user_data = {html.escape(str(context.user_data))}\n\n"
            f"{html.escape(tb_string)}"
        )
        with io.BytesIO(str.encode(message)) as out_file:
            out_file.name = "error logs.txt"
            await context.bot.send_document(
                chat_id=TOPIC_ID,
                document=out_file,
                message_thread_id=TOPIC_THREADS["error"],
            )
    else:
        await context.bot.send_message(
            chat_id=TOPIC_ID,
            text=message,
            parse_mode=ParseMode.HTML,
            message_thread_id=TOPIC_THREADS["error"],
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat
    if (
        int(chat.id) == int(TOPIC_ID)
        and message.message_thread_id == TOPIC_THREADS["fun"]
    ):
        msg = f"Echo: {message.text.split('/echo ')[1]}"
        await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id != int(OWNER_ID):
        return

    message = update.effective_message
    reply_to = message.reply_to_message
    if not reply_to:
        return await message.reply_text(
            "Please reply to some message in order to publish it."
        )

    await reply_to.copy(int(TOPIC_ID), message_thread_id=TOPIC_THREADS["updates"])


def main() -> None:
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("announce", announce))
    application.add_error_handler(error_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    LOGGER.info("Bot Started.")

    main()
