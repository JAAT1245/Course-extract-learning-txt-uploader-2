import os
import re
import sys
import requests
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyromod import listen
import time

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

    await editable.edit("📝 **Send the batch name:**")
    input1: Message = await bot.listen(editable.chat.id)
    batch_name = input1.text
    await input1.delete(True)

    await editable.edit(
        "📸 **Choose a resolution (for videos):**\n144, 240, 360, 480, 720, 1080"
    )
    input2: Message = await bot.listen(editable.chat.id)
    resolution = input2.text
    await input2.delete(True)

    await editable.edit("✍️ **Enter a caption for the uploaded file:**")
    input3: Message = await bot.listen(editable.chat.id)
    caption = input3.text
    await input3.delete(True)

    await editable.edit("🌄 **Send a thumbnail URL or type 'no':**")
    input6 = await bot.listen(editable.chat.id)
    thumb_url = input6.text
    await input6.delete(True)
    await editable.delete()

    # Download thumbnail if provided
    thumb_path = None
    if thumb_url.startswith("http"):
        thumb_path = "thumb.jpg"
        os.system(f"wget '{thumb_url}' -O {thumb_path}")

    raw_text0 = batch_name
    raw_text2 = resolution
    count = start_link

    # Start video download processing
    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + V

            # VisionIAS URL handling
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'User-Agent': 'Mozilla/5.0'}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            # ClassPlusApp URL handling
            elif 'videos.classplusapp' in url:
                url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}',
                                   headers={'x-access-token': 'your_token_here'}).json()['url']

            # Master.mpd URL handling
            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # YouTube specific format
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"

            # yt-dlp command
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                os.system(cmd)

                # Send the video file with the caption
                cc = f'**[📽️] Vid_ID:** {str(count).zfill(3)}.** {name1}{MR}.mkv\n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**,>>JOIN @TARGETALLCOURSE'
                cc1 = f'**[📁] Pdf_ID:** {str(count).zfill(3)}. {name1}{MR}.pdf \n**𝔹ᴀᴛᴄʜ** » **{raw_text0}**,>>JOIN @TARGETALLCOURSE'

                # Send the video file with the caption
                await bot.send_document(chat_id=m.chat.id, document=f"{name}.mp4", caption=cc, thumb=thumb_path)

                # Clean up the downloaded video
                os.remove(f"{name}.mp4")
                count += 1
            except Exception as e:
                await m.reply_text(f"❌ **Error Downloading {name}:** {e}")
                continue

    except Exception as e:
        await m.reply_text(f"❌ **Error:** {e}")

    # Clean up the thumbnail
    if thumb_path and os.path.exists(thumb_path):
        os.remove(thumb_path)

# Running the bot
bot.run()
