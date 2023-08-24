import logging
import sqlite3
from aiogram import Bot,Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode

API_Token = "6465672744:AAHmhs_yporVQ_iRKeuWd3g39t9YIDccHso"
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
islomiy_kitoblar=ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text="📖 Qur'oni karim ma'nolarini tarjimasi"),
            KeyboardButton(text="📖 Tarixi Muhammadiy")],

            [KeyboardButton(text="📖 Temur tuzuklari"),
            KeyboardButton(text="📖 Til ofatlari")],

            [KeyboardButton(text="📖 Abdulloh Murod. Qalbimizning nuri"),
            KeyboardButton(text="📖 Alhamdulillah")],

            [KeyboardButton(text="📖 Haj-amallari"),
            KeyboardButton(text="📖 Hijobim")],

            [KeyboardButton(text="📖 Horun Yahyo Qur'on axloqiga ko'ra"),
            KeyboardButton(text="📖 Ibodat va zikr ahliga tavsiyalar")],

            [KeyboardButton(text="📖 Imom G'azzoliy. Ihyou ulumid-din"),
            KeyboardButton(text="📖 Imom Shamsuddin Zahabiy. Gunohi kabiralar")],

            [KeyboardButton(text="📖 Jajji musulmonlar uchun Tahorat olish tartibi"),
            KeyboardButton(text="📖 Jannat-ahli")],

            [KeyboardButton(text="📖 Juma kuni öqiladigan salovatlar"),
            KeyboardButton(text="📖 Namozda xushu")],

            [KeyboardButton(text="📖 namoz-moʻminning-meʼrojidir"),
            KeyboardButton(text="📖 payg'ambar uyida 1 kun")],

            [KeyboardButton(text="📖 Qachon tavba qilasan"),
            KeyboardButton(text="📖 Quron yodlash fazilatlari")],

            [KeyboardButton(text="📖 Usmon roziyallohu anhuning fazilatlari"),
            KeyboardButton(text="📖 Zohidjon Islomov. Musulmonning odob kitobi")],

            [KeyboardButton(text="📖 Qalb kasaliklari va munofiqlik"),
            KeyboardButton(text="📖 Tahorat kitobi")],



            [KeyboardButton(text="⬅️ Orqaga")],

            ],
    resize_keyboard=True
)

detektiv_kitoblar=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔎📒 Da Vinchi siri"),
            KeyboardButton(text="🔎📒 Dang‘illama hovlidagi o‘lim")],

            [KeyboardButton(text="🔎📒 Farengeyt bo‘yicha 451 daraja"),
            KeyboardButton(text="🔎📒 Graf Monte Kristo")],

            [KeyboardButton(text="🔎📒 Ityurak"),
            KeyboardButton(text="🔎📒 Jinoyat va jazo")],

            [KeyboardButton(text="🔎📒 Mario Pyuzo. Cho‘qintirgan ota"),
            KeyboardButton(text="🔎📒 O‘g‘irlangan million dollar")],

            [KeyboardButton(text="🔎📒 Shaytanat 1-kitob"),
            KeyboardButton(text="🔎📒 Shaytanat 2-kitob")],

            [KeyboardButton(text="🔎📒 Shaytanat 3-kitob"),
            KeyboardButton(text="🔎📒 Shaytanat 4-kitob")],

            [KeyboardButton(text="🔎📒 Sherlok Xolms haqida hikoyalar"),
            KeyboardButton(text="🔎📒 Tokio vaqti bilan oltiyu o'ttizda")],

            [KeyboardButton(text="⬅️ Orqaga")]
        ,
    ],
    resize_keyboard=True
)

boshqa_kitoblar=ReplyKeyboardMarkup(
    keyboard=[

            [KeyboardButton(text="📚 Boy ota,Kambag'al ota"),
            KeyboardButton(text="📚 Millioner singari fikrlashni o‘rganing")],

            [KeyboardButton(text="📚 Pul topish sirlari"),
             KeyboardButton(text="📚 Raqamlar uchun yaralgan idrok")],

            [KeyboardButton(text="📚 Robin Sharma - 200 sir"),
             KeyboardButton(text="📚 Xulosat ul-hukamo (hakimlar xulosasi)")],

            [KeyboardButton(text="⬅️ Orqaga")],

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
        await message.reply(f"Assalomu alaykum {message.from_user.full_name}! Kitoblar olamiga xush kelibsiz! Botdan foydalanish uchun 'Kirish' tugmasini bosing! ",
                            reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Asosiy menyuga o'tish uchun Kirish tugmasini bosing!",
                             reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 types.KeyboardButton("Kirish", request_contact=True)))


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
    await xabar.answer(f"📖 Islomiy Kitobni ko'rishingiz mumkun!",reply_markup=islomiy_kitoblar)

BASE_DIRECTORY = "islomiy_kitoblar/"
@dp.message_handler(lambda message: message.text == "📖 Qur'oni karim ma'nolarini tarjimasi")
async def send_detective_books(message: types.Message):
    pdf_file="Qur'oni karim ma'nolari tarjimasi.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Tarixi Muhammadiy")
async def send_detective_books(message: types.Message):
    pdf_file="Tarixi Muhammadiy.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Temur tuzuklari")
async def send_detective_books(message: types.Message):
    pdf_file="Temur tuzuklari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Til ofatlari")
async def send_detective_books(message: types.Message):
    pdf_file="Til ofatlari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Abdulloh Murod. Qalbimizning nuri")
async def send_detective_books(message: types.Message):
    pdf_file="Abdulloh Murod. Qalbimizning nuri.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Alhamdulillah")
async def send_detective_books(message: types.Message):
    pdf_files="Alhamdulillah.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_files
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Haj-amallari")
async def send_detective_books(message: types.Message):
    pdf_file= "Haj-amallari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Hijobim")
async def send_detective_books(message: types.Message):
    pdf_file= "Hijobim.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Horun Yahyo Qur'on axloqiga ko'ra")
async def send_detective_books(message: types.Message):
    pdf_file="Horun_Yahyo_Qur'on_axloqiga_ko'ra.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Ibodat va zikr ahliga tavsiyalar")
async def send_detective_books(message: types.Message):
    pdf_file="Ibodat va zikr ahliga tavsiyalar.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Imom G'azzoliy. Ihyou ulumid-din")
async def send_detective_books(message: types.Message):
    pdf_file="Imom G'azzoliy. Ihyou ulumid-din.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Imom Shamsuddin Zahabiy. Gunohi kabiralar")
async def send_detective_books(message: types.Message):
    pdf_file="Imom Shamsuddin Zahabiy. Gunohi kabiralar.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Jajji musulmonlar uchun Tahorat olish tartibi")
async def send_detective_books(message: types.Message):
    pdf_file="Jajji musulmonlar uchun Tahorat olish tartibi.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📖 Jannat-ahli")
async def send_detective_books(message: types.Message):
    pdf_file="Jannat-ahli.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📖 Juma kuni öqiladigan salovatlar")
async def send_detective_books(message: types.Message):
    pdf_file="Juma kuni öqiladigan salovatlar.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📖 Namozda xushu")
async def send_detective_books(message: types.Message):
    pdf_file="Namozda xushu.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📖 namoz-moʻminning-meʼrojidir")
async def send_detective_books(message: types.Message):
    pdf_file="namoz-moʻminning-meʼrojidir.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📖 payg'ambar uyida 1 kun")
async def send_detective_books(message: types.Message):
    pdf_file="payghambar uyida 1 kun.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Qachon tavba qilasan")
async def send_detective_books(message: types.Message):
    pdf_file="Qachon tavba qilasan.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Quron yodlash fazilatlari")
async def send_detective_books(message: types.Message):
    pdf_file="Quron yodlash fazilatlari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Usmon roziyallohu anhuning fazilatlari")
async def send_detective_books(message: types.Message):
    pdf_file="Usmon roziyallohu anhuning fazilatlari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Zohidjon Islomov. Musulmonning odob kitobi")
async def send_detective_books(message: types.Message):
    pdf_file="Zohidjon Islomov. Musulmonning odob kitobi.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Qalb kasaliklari va munofiqlik")
async def send_detective_books(message: types.Message):
    pdf_file="Qalb kasaliklari va munofiqlik.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "📖 Tahorat kitobi")
async def send_detective_books(message: types.Message):
    pdf_file="Tahorat kitobi .pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = BASE_DIRECTORY + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)




@dp.message_handler(text="🔎📒 Detektiv kitoblar")
async def insta_down(xabar:types.Message):
    await xabar.answer(f"🔎📒 Detektiv kitoblarni ko'rishingiz mumkun!",reply_markup=detektiv_kitoblar)

fayl_detektiv="detektiv_kitoblar/"

@dp.message_handler(lambda message: message.text == "🔎📒 Da Vinchi siri")
async def send_detective_books(message: types.Message):
    pdf_file="Da Vinchi siri.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Dang‘illama hovlidagi o‘lim")
async def send_detective_books(message: types.Message):
    pdf_file="Dang‘illama hovlidagi o‘lim.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Farengeyt bo‘yicha 451 daraja")
async def send_detective_books(message: types.Message):
    pdf_file="Farengeyt bo‘yicha 451 daraja.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Graf Monte Kristo")
async def send_detective_books(message: types.Message):
    pdf_file="Graf Monte Kristo.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Ityurak")
async def send_detective_books(message: types.Message):
    pdf_file="Ityurak.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Jinoyat va jazo")
async def send_detective_books(message: types.Message):
    pdf_file="Jinoyat va jazo.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Mario Pyuzo. Cho‘qintirgan ota")
async def send_detective_books(message: types.Message):
    pdf_file="Mario Pyuzo. Cho‘qintirgan ota.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 O‘g‘irlangan million dollar")
async def send_detective_books(message: types.Message):
    pdf_file="O‘g‘irlangan million dollar.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Shaytanat 1-kitob")
async def send_detective_books(message: types.Message):
    pdf_file="Shaytanat 1-kitob.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Shaytanat 2-kitob")
async def send_detective_books(message: types.Message):
    pdf_file="Shaytanat 2-kitob.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "🔎📒 Shaytanat 3-kitob")
async def send_detective_books(message: types.Message):
    pdf_file="Shaytanat 3-kitob.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Shaytanat 4-kitob")
async def send_detective_books(message: types.Message):
    pdf_file="Shaytanat 4-kitob.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "🔎📒 Sherlok Xolms haqida hikoyalar")
async def send_detective_books(message: types.Message):
    pdf_file="Sherlok Xolms haqida hikoyalar.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(lambda message: message.text == "🔎📒 Tokio vaqti bilan oltiyu o'ttizda")
async def send_detective_books(message: types.Message):
    pdf_file="Tokio vaqti bilan oltiyu o'ttizda.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_detektiv + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(text="📚 Barcha kitoblar")
async def insta_down(xabar:types.Message):
    await xabar.answer(f"📚 Barcha kitoblarni ko'rishingiz mumkun!",reply_markup=boshqa_kitoblar)
fayl_boshqa_kitoblar="file/"

@dp.message_handler(lambda message: message.text == "📚 Boy ota,Kambag'al ota")
async def send_detective_books(message: types.Message):
    pdf_file="Boy ota,Kambag'al ota.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📚 Millioner singari fikrlashni o‘rganing")
async def send_detective_books(message: types.Message):
    pdf_file="Millioner singari fikrlashni o‘rganing.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📚 Pul topish sirlari")
async def send_detective_books(message: types.Message):
    pdf_file="Pul topish sirlari.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📚 Raqamlar uchun yaralgan idrok")
async def send_detective_books(message: types.Message):
    pdf_file="Raqamlar uchun yaralgan idrok.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📚 Robin Sharma - 200 sir")
async def send_detective_books(message: types.Message):
    pdf_file="Robin Sharma - 200 sir.pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)

@dp.message_handler(lambda message: message.text == "📚 Xulosat ul-hukamo (hakimlar xulosasi)")
async def send_detective_books(message: types.Message):
    pdf_file="Xulosat ul-hukamo (hakimlar xulosasi).pdf"
    await message.reply("Biroz kuting,Kitob yuklanmoqda...")
    pdf_path = fayl_boshqa_kitoblar + pdf_file
    with open(pdf_path, 'rb') as pdf:
        await bot.send_document(message.chat.id, pdf)
@dp.message_handler(text="⬅️ Orqaga")
async def instsa_down(xabar:types.Message):
    await xabar.answer(f"Kitoblar bo`limi : ",reply_markup=main_menu)


# BASE_DIRECTORY = "file/"
# @dp.message_handler(lambda message: message.text == "🔎📒 Detektiv kitoblar")
# async def send_detective_books(message: types.Message):
#     pdf_files = [
#         "Mustaqil talimTTT.docx",
#
#
#     ]
#
#     for pdf_file in pdf_files:
#         pdf_path = BASE_DIRECTORY + pdf_file
#         with open(pdf_path, 'rb') as pdf:
#             await bot.send_document(message.chat.id, pdf)






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