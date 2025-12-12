import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

bot = Client("romio-simple-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("romio-simple-user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call = PyTgCalls(user)

def download_audio(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "quiet": True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        return ydl.prepare_filename(info)

@bot.on_message(filters.command("play") & filters.group)
async def play_command(_, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Please send a song name or YouTube link!\nExample: `/play love me like you do`")

    query = message.text.split(None, 1)[1]
    msg = await message.reply("🎵 Downloading audio...")

    file = download_audio(query)

    await call.join_group_call(
        message.chat.id,
        InputStream(file, HighQualityAudio())
    )

    await msg.edit("▶ **Now Playing Music in Voice Chat!**")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_command(_, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⛔ Music Stopped!")

async def main():
    await user.start()
    await bot.start()
    await call.start()
    print("Romio Simple Music Bot is Running...")
    await idle()

from pytgcalls import idle
import asyncio
asyncio.run(main())
