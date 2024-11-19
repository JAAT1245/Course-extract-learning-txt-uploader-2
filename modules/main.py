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
    editable = await m.reply_text(
        f"✨ **Welcome, [{m.from_user.first_name}](tg://user?id={m.from_user.id})!** ✨\n\n"
        "🔥 **I'm here to make your experience awesome!**\n"
        "🚀 Press **/crchoudhary** to explore my features and get started!\n\n"
        "💡 Need help? Just type /help anytime."
    )

@bot.on_message(filters.command(["help"]))
async def help_command(bot: Client, m: Message):
    await m.reply_text(
        f"💡 **Hello, [{m.from_user.first_name}](tg://user?id={m.from_user.id})!**\n\n"
        "🌟 Here's how I can assist you:\n\n"
        "🔹 **/start** - To restart the bot and get a fresh welcome.\n"
        "🔹 **/crchoudhary** - Explore my exclusive features.\n"
        "🔹 **/help** - To see this help JOIN @TARGETALLCOURSE anytime.\n\n"
        "✨ **More commands coming soon! Stay tuned.**\n\n"
        "⚡ Need further assistance? Feel free to ask!"
    )
    
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
    highlighter  = f"️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'Robin':
        MR = highlighter 
    else:
        MR = raw_text3
   
    await editable.edit("Now send the Thumb url/nEg » https://graph.org/file/3d4562c52f26a50809325.jpg \n Or if don't want thumbnail send = no")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

   

    try:
          for i in range(count - 1, len(links)):

        V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
        url = "https://" + V

        if "visionias" in url:
            async with ClientSession() as session:
                async with session.get(url, headers={...}) as resp:  # (Headers unchanged from your original code)
                    text = await resp.text()
                    url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

        elif 'videos.classplusapp' in url:
            url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={...}).json()['url']  # Token unchanged

        elif '/master.mpd' in url:
            id = url.split("/")[-2]
            url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

        name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
        name = f'{str(count).zfill(3)}) {name1[:60]}'

        if "youtu" in url:
            ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
        else:
            ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

        if "jw-prod" in url:
            cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
        else:
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

        try:  
            cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}. {name1}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**,>>JOIN @TARGETALLCOURSE'
            cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**,>>JOIN @TARGETALLCOURSE'
            
            if "drive" in url:
                try:
                    ka = await helper.download(url, name)
                    # Send to user's chat
                    await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                    # Send to permanent channel
                    await bot.send_document(chat_id=PERMANENT_CHANNEL, document=ka, caption=cc1)
                    count += 1
                    os.remove(ka)
                    time.sleep(1)
                except FloodWait as e:
                    await m.reply_text(str(e))
                    time.sleep(e.x)
                    continue
            
            elif ".pdf" in url:
                try:
                    cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                    download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                    os.system(download_cmd)
                    # Send to user's chat
                    await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                    # Send to permanent channel
                    await bot.send_document(chat_id=PERMANENT_CHANNEL, document=f'{name}.pdf', caption=cc1)
                    count += 1
                    os.remove(f'{name}.pdf')
                except FloodWait as e:
                    await m.reply_text(str(e))
                    time.sleep(e.x)
                    continue
            else:
                Show = f"**⥥ 🄳🄾🅆🄽🄻🄾🄰🄳🄸🄽🄶⬇️⬇️... »**\n\n**📝Name »** `{name}\n❄Quality » {raw_text2}`\n\n**🔗URL »** `{url}`"
                prog = await m.reply_text(Show)
                res_file = await helper.download_video(url, cmd, name)
                filename = res_file
                await prog.delete(True)
                # Send to user's chat
                await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                # Send to permanent channel
                await bot.send_video(chat_id=PERMANENT_CHANNEL, video=filename, caption=cc, thumb=thumb)
                count += 1
                time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"**downloading Interupted **\n{str(e)}\n**Name** » {name}\n**Link** » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done 𝔹ᴏ𝕤𝕤🔰 ")


bot.run()

