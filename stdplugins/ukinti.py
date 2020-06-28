""" @ukinti_bot
Available Commands:
.unbanall
.kick option
Available Options: d, y, m, w, o, q, r """
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
from datetime import datetime, timedelta
from time import sleep

from telethon import events
from telethon.tl import functions, types
from telethon.tl.types import (ChannelParticipantsKicked, ChatBannedRights,
                               UserStatusEmpty, UserStatusLastMonth,
                               UserStatusLastWeek, UserStatusOffline,
                               UserStatusOnline, UserStatusRecently)

from uniborg.util import admin_cmd

from sample_config import Config


@borg.on(admin_cmd(pattern="unbanall ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        await event.edit("Searching Participant Lists.")
        p = 0
        async for i in borg.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(
                until_date=0,
                view_messages=False
            )
            try:
                await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await event.edit(str(ex))
            else:
                p += 1
        await event.edit("{}: {} unbanned".format(event.chat_id, p))


@borg.on(admin_cmd(pattern="kick ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await event.edit("`You aren't an admin here!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    await event.edit("Searching Participant Lists.")
    async for i in borg.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
                    break
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await event.edit("I need admin priveleges to perform this action!")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}"""
        await event.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await asyncio.sleep(5)
    await event.edit("""Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
Bots: {}
None: {}""".format(p, d, y, m, w, o, q, r, b, n))


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)
