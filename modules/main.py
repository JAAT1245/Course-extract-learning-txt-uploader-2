import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import api_id, api_hash, bot_token
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)


PERMANENT_CHANNEL = "@Hub_formate"  # Replace with your permanent channel username or ID

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nPress /crchoudhary")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["crchoudhary"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text('𝕋𝕆 ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴛxᴛ ғɪʟᴇ 𝕤ᴇɴᴅ ʜᴇʀᴇ ⚡️')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(False)

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = [i.split("://", 1) for i in content]
        os.remove(x)
    except:
        await m.reply_text("**Invalid file input.**")
        os.remove(x)
        return
    
    await editable.edit(f"**𝕋ᴏᴛᴀʟ ʟɪɴᴋ𝕤 ғᴏᴜɴᴅ ᴀʀᴇ🔗🔗** **{len(links)}**\n\n**𝕊ᴇɴᴅ 𝔽ʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪ𝕤** **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Now Please Send Me Your Batch Name**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)

    await editable.edit("**𝔼ɴᴛᴇʀ ʀᴇ𝕤ᴏʟᴜᴛɪᴏɴ📸**\n144,240,360,480,720,1080 please choose quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)

    res = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }.get(raw_text2, "UN")

    await editable.edit("Now Enter A Caption to add caption on your uploaded file")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)

    highlighter = "️ ⁪⁬⁮⁮⁮"
    MR = highlighter if raw_text3 == 'Robin' else raw_text3

    await editable.edit("Now send the Thumb URL (or type 'no' if you don't want a thumbnail)")
    input6: Message = await bot.listen(editable.chat.id)
    thumb = input6.text
    await input6.delete(True)

    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = "no"

    count = int(raw_text) if len(links) > 1 else 1

    try:
        for i in range(count - 1, len(links)):
            url = "https://" + links[i][1]
            name1 = links[i][0].replace("\t", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            cc = f"**[📽️] Vid_ID:** {str(count).zfill(3)}. **{name1}{MR}.mkv**\n**Batch** » **{raw_text0}**,JOIN @TARGETALLCOURSE"
            cc1 = f"**[📁] Pdf_ID:** {str(count).zfill(3)}. **{name1}{MR}.pdf**\n**Batch** » **{raw_text0}**,JOIN @TARGETALLCOURSE"

            if "drive" in url or ".pdf" in url:
                try:
                    ka = await helper.download(url, name)
                    copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    # Forward the document to the permanent channel
                    await bot.send_document(chat_id=PERMANENT_CHANNEL, document=ka, caption=cc1)
                    count += 1
                    os.remove(ka)
                    time.sleep(1)
                except FloodWait as e:
                    await m.reply_text(str(e))
                    time.sleep(e.x)
                    continue
            else:
                prog = await m.reply_text(f"**Downloading...**\n**Name:** `{name}`\n**Quality:** `{raw_text2}`")
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await prog.delete(True)
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                # Forward the video to the permanent channel
                await bot.send_video(chat_id=PERMANENT_CHANNEL, video=filename, caption=cc, thumb=thumb)
                count += 1
                time.sleep(1)

    except Exception as e:
        await m.reply_text(f"Error: {e}")
    await m.reply_text("🔰Done Boss🔰")

bot.run()
