import os
import time
import math
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


#README DOSYASINDA YAZAN ŞEYLERİ BURAYA DOLDURUN
api_id = 
api_hash = ''
bot_token = ''



app = Client("oktayyavuz", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  
CHUNK_SIZE = 1.5 * 1024 * 1024 * 1024 

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Merhaba! YouTube video linkini gönderin, ben de indirip size göndereyim.")

@app.on_message(filters.text & ~filters.create(lambda _, __, message: message.text.startswith('/')))
async def send_quality_buttons(client, message):
    url = message.text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("1080p", callback_data=f"1080p|{url}")],
        [InlineKeyboardButton("720p", callback_data=f"720p|{url}")],
        [InlineKeyboardButton("480p", callback_data=f"480p|{url}")],
    ])
    await message.reply_text("📺 Kalite seçin:", reply_markup=keyboard)

@app.on_callback_query()
async def download_video(client, callback_query):
    quality, url = callback_query.data.split('|')
    chat_id = callback_query.message.chat.id

    ydl_opts = {
        'format': f'bestvideo[ext=mp4][height<={quality[:-1]}]+bestaudio[ext=m4a]/best[ext=mp4][height<={quality[:-1]}]',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
    }

    await callback_query.message.delete()  

    waiting_message = await callback_query.message.reply_text("📥 Video indiriliyor, lütfen bekleyin...")

    start_time = time.time()

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info_dict)
            video_title = info_dict.get('title', 'Video')

            elapsed_time = time.time() - start_time
            await waiting_message.edit_text(f"📥 Video indirildi. Geçen süre: {int(elapsed_time)} saniye. Gönderiliyor...")

            file_size = os.path.getsize(video_file)

            if file_size > MAX_FILE_SIZE:
                await callback_query.message.reply_text("⚠️ Video dosyası 2GB'den büyük, bu nedenle parçalara bölünüyor.")
                await send_large_file_via_pyrogram(client, chat_id, video_file, video_title, callback_query)
            else:
                start_time = time.time() 
                last_update_time = start_time

                async def progress_callback(current, total):
                    nonlocal last_update_time
                    elapsed_time = time.time() - start_time
                    percent_complete = current / total * 100
                    eta = (total - current) / (current / elapsed_time) if current > 0 else 0

                    if time.time() - last_update_time >= 5:  
                        await waiting_message.edit_text(
                            f"🔄 Yükleniyor: %{percent_complete:.2f}\n"
                            f"⏳ Geçen Süre: {int(elapsed_time)} saniye\n"
                            f"📅 Tahmini Süre: {int(eta)} saniye"
                        )
                        last_update_time = time.time()

                await client.send_video(chat_id, video_file, caption=video_title, progress=progress_callback)
            
            os.remove(video_file)
    
    except Exception as e:
        await waiting_message.edit_text(f"❌ Bir hata oluştu: {e}")

    await waiting_message.delete()  

async def send_large_file_via_pyrogram(client, chat_id, video_file, video_title, callback_query):
    total_size = os.path.getsize(video_file)
    num_parts = math.ceil(total_size / CHUNK_SIZE)
    video_duration = get_video_duration(video_file)  

    for part_num in range(num_parts):
        start_time = time.time()
        progress_message = await callback_query.message.reply_text(f"📤 {part_num + 1}. parça gönderiliyor...")

        part_file = f"{video_file}_part{part_num + 1}.mp4"
        start_sec = part_num * (video_duration / num_parts)
        end_sec = min((part_num + 1) * (video_duration / num_parts), video_duration)

        ffmpeg_extract_subclip(video_file, start_sec, end_sec, targetname=part_file)

        last_update_time = start_time  

        async def progress_callback(current, total):
            nonlocal last_update_time
            elapsed_time = time.time() - start_time
            percent_complete = current / total * 100
            eta = (total - current) / (current / elapsed_time) if current > 0 else 0
            
            if time.time() - last_update_time >= 5:  
                await progress_message.edit_text(
                    f"🔄 Yükleniyor: %{percent_complete:.2f}\n"
                    f"⏳ Geçen Süre: {int(elapsed_time)} saniye\n"
                    f"📅 Tahmini Süre: {int(eta)} saniye"
                )
                last_update_time = time.time()

        await client.send_video(
            chat_id,
            part_file,
            caption=f"{video_title} - Part {part_num + 1}",
            progress=progress_callback,
            file_name=os.path.basename(part_file),
        )

        await progress_message.edit_text(f"✅ {part_num + 1}. parça başarıyla gönderildi.")
        os.remove(part_file)

    await callback_query.message.reply_text(f"✅ Tüm parçalar başarıyla gönderildi.")

def get_video_duration(video_file):
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

if __name__ == "__main__":
    app.run()
