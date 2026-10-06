from telegram import Update
from telegram.ext import ContextTypes
# ----------------------------------------------------- #


async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return None
    else:
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text="Bot is runnig\nFor use this bot use /help",
            reply_to_message_id=update.message.message_id,
        )
        return None


async def help_cmd(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    
    return None
