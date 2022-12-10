from telethon.events import NewMessage, StopPropagation

from .bind_chat import bind_chat, trigger_bind_chat
from .check_chat import check_chat, trigger_check_chat
from .start import start, trigger_start


# https://docs.telethon.dev/en/latest/concepts/updates.html#stopping-propagation-of-updates
async def handle_start(event: NewMessage):
    await start(event)
    raise StopPropagation


async def handle_bind_chat(event: NewMessage):
    await bind_chat(event)
    raise StopPropagation


async def handle_check_chat(event: NewMessage):
    await check_chat(event)
    raise StopPropagation
