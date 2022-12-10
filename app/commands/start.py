import logging
import re

from telethon import events
from telethon.tl import types

logger = logging.getLogger(__name__)


async def start(
    event: events.NewMessage,
    sender: types.User = None,
):
    # help - https://docs.telethon.dev/en/latest/basic/updates.html#entities

    chat = await event.get_chat()
    chat_id = event.chat_id
    if sender is None:
        sender = await event.get_sender()
    if not isinstance(chat, types.Chat):
        logger.info("bot activated in pm")
        await event.reply(f"Hi user {sender.id}!")
    else:
        logger.info("bot activated in chat")
        await event.reply(f"Hi chat {chat_id}!")


def trigger_start():
    return [
        events.NewMessage(
            pattern=re.compile("^/start", flags=re.M | re.I), incoming=True
        )
    ]
