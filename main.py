import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.stream import StreamAudioEnded
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

bot = Client("RomioBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("RomioUser", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

call = PyTgCalls(user)

@bot.on_message(filters.command("play") & filters.group)
async def play_handler(_, message):
    if len(message.command) < 2:
        return await message.reply("❗ Song name or link bhi likho bhai.")

    query = message.text.split(None, 1)[1]
    msg = await message.reply("🎵 Streaming... please wait")

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info["url"]

    await call.join_group_call(
        message.chat.id,
        AudioPiped(url)
    )

    await msg.edit(f"▶ **Now Streaming:** {info.get('title', 'audio')}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_handler(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⛔ Stream Stopped.")

async def main():
    await user.start()
    await bot.start()
    await call.start()
    print("RomioBot is running...")
    await idle()

from pytgcalls import idle
import asyncio
asyncio.run(main())
