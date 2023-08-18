import logging
import sqlite3
from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

API_Token = "6465672744:AAGeSnhv5a94OwythYFi8dtA4k7Uvzrf4K4"
logging.basicConfig(level=logging.INFO)
DATABASE_NAME = 'user_data.db'

bot = Bot(API_Token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        phone_number TEXT
    )
''')
conn.commit()


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📖 Islomiy kitoblar"),
            KeyboardButton(text="🔎📒 Detektiv kitoblar"),
            KeyboardButton(text="📚 Barcha kitoblar")
        ],
    ],
    resize_keyboard=True
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        await message.reply("Siz allaqachon ro'yxatdan o'tgansiz.")
        await message.reply("Quyidagi menyu orqali kitob turini tanlang:", reply_markup=main_menu)
    else:
        await message.reply(f"Assalomu alaykum {message.from_user.full_name}! Kitoblar olamiga xush kelibsiz! Botdan foydalanish uchun registratsiydan o'ting! Iltimos, telefon raqamingizni ulashing.",
                            reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Telefon raqamingizni yuborish uchun tugmani bosing.",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 types.KeyboardButton("Telefon raqamni yuborish", request_contact=True)))


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    phone_number = message.contact.phone_number

    cursor.execute('INSERT INTO users (id, username, phone_number) VALUES (?, ?, ?)', (user_id, username, phone_number))
    conn.commit()

    await message.reply(f"Telefon raqamingizni ulashganingiz uchun rahmat! Sizning telefon raqamingiz:📞 {phone_number}.Marxamat,Botimizdan foydalanishingiz mumkun!", parse_mode=ParseMode.MARKDOWN)
    await message.reply("Quyidagi menyu orqali kitob turini tanlang:", reply_markup=main_menu)

@dp.message_handler(text="📖 Islomiy kitoblar")
async def insta_down(xabar:types.Message):
    await xabar.answer(f"📖 Islomiy Kitobni ushbu havoladan yuklab olishingiz mumkin:https://t.me/+RyIFcVYlmgIzYTY6 ")


@dp.message_handler(lambda message: message.text == "🔎📒 Detektiv kitoblar")
async def send_detective_books(message: types.Message):
    # file_id = 457
    # file_link = f"https://t.me/c/1739233391/{file_id}"
    await bot.send_message(message.chat.id, f"🔎📒 Detektiv Kitobni ushbu havoladan yuklab olishingiz mumkin:https://t.me/+RyIFcVYlmgIzYTY6")


@dp.message_handler(text="📚 Barcha kitoblar")
async def insta_down(xabar:types.Message):
    await xabar.answer(f"📚 Barcha kitoblarni ushbu havoladan yuklab olishingiz mumkin:https://t.me/+RyIFcVYlmgIzYTY6 ")




@dp.message_handler(commands='kali')
async def kali_command(message: types.Message):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT username, phone_number FROM users')
    user_data = cursor.fetchall()

    conn.close()

    if user_data:
        result_message = "Foydalanuvchilar ma'lumotlari:\n"
        sanoq=0
        for username, phone_number in user_data:
            sanoq+=1
            result_message += f"Username: @{username}, Telefon raqami: {phone_number}\n"
    else:
        result_message = "Foydalanuvchi ma'lumotlari topilmadi."

    await message.answer(f"{result_message}\n ___________________________________ \nBotdan foydalanuvchilar soni: {sanoq} ta")




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)