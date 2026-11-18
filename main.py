from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import yt_dlp
import os

TOKEN = "9185090598:AAGPTyedUSUQLkt76fD1ez4BiliFw1lyFrk"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(lambda message: message.text == '/start')
async def send_welcome(message: types.Message):
    await message.answer("Assalomu alaykum! Men MusicBot'man. Menga istalgan qo'shiq yoki video havolasini yuboring, uni MP3 formatiga o'tkazib beraman!")

# Havola kelganda ishlaydigan qism
@dp.message()
async def download_music(message: types.Message):
    url = message.text
    if not url.startswith("http"):
        await message.answer("Iltimos, to'g'ri havola (link) yuboring!")
        return

    await message.answer("Musiqa yuklab olinmoqda va MP3 ga o'girilmoqda, biroz kuting...")

    try:
        # yt-dlp sozlamalari (faqat mp3 formatida yuklash uchun)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'song.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_file = "song.mp3"
        
        if os.path.exists(audio_file):
            audio = types.FSInputFile(audio_file)
            await message.answer_audio(audio)
            os.remove(audio_file) # Faylni yuborgach kompyuterdan o'chiramiz
        else:
            await message.answer("Kechirasiz, faylni yuklab bo'lmadi.")

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    print("Bot ishga tushdi va musiqalarni qabul qilishga tayyor...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())