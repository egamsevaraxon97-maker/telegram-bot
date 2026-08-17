import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Token endi kompyuterdagi fayl ichida emas, Render'ning
# Environment Variables bo'limidan BOT_TOKEN nomi bilan olinadi.
# Lokal kompyuterda sinash uchun pastdagi qatorni vaqtincha
# o'zgartirib turishingiz mumkin: os.getenv("BOT_TOKEN", "TOKENINGIZ")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8635012488:AAFyTScV-mJnKiZmqo6uF9Vanr5UOeL0-v4")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ------------------------------------------------------------
# Har bir mavzu uchun tayyor namuna kod va tushuntirish
# ------------------------------------------------------------

LESSONS = {
    "print": {
        "title": "🖨 print() funksiyasi",
        "text": (
            "print() — ekranga ma'lumot chiqaradi.\n\n"
            "```python\n"
            "print(\"Salom, dunyo!\")\n"
            "print(5 + 3)\n"
            "print(\"Yosh:\", 25)\n"
            "```\n\n"
            "Natija:\n"
            "Salom, dunyo!\n"
            "8\n"
            "Yosh: 25"
        ),
    },
    "def": {
        "title": "🧩 Funksiya yaratish (def)",
        "text": (
            "def — o'z funksiyangizni yaratish uchun ishlatiladi.\n\n"
            "```python\n"
            "def salomlash(ism):\n"
            "    print(f\"Salom, {ism}!\")\n\n"
            "salomlash(\"Aziz\")\n"
            "```\n\n"
            "Natija:\n"
            "Salom, Aziz!"
        ),
    },
    "return": {
        "title": "↩️ return operatori",
        "text": (
            "return — funksiyadan natija qaytaradi, uni saqlab qo'yish mumkin.\n\n"
            "```python\n"
            "def kvadrat(son):\n"
            "    return son * son\n\n"
            "natija = kvadrat(4)\n"
            "print(natija)\n"
            "```\n\n"
            "Natija:\n"
            "16"
        ),
    },
    "if": {
        "title": "🔀 Shart operatori (if / elif / else)",
        "text": (
            "if — shartga qarab dastur yo'nalishini tanlaydi.\n\n"
            "```python\n"
            "yosh = 20\n"
            "if yosh < 18:\n"
            "    print(\"Voyaga yetmagan\")\n"
            "elif yosh < 60:\n"
            "    print(\"Kattalar\")\n"
            "else:\n"
            "    print(\"Pensioner\")\n"
            "```\n\n"
            "Natija:\n"
            "Kattalar"
        ),
    },
    "for": {
        "title": "🔁 for sikli",
        "text": (
            "for — ro'yxat yoki ketma-ketlik bo'ylab aylanadi.\n\n"
            "```python\n"
            "mevalar = [\"olma\", \"nok\", \"uzum\"]\n"
            "for meva in mevalar:\n"
            "    print(meva)\n"
            "```\n\n"
            "Natija:\n"
            "olma\n"
            "nok\n"
            "uzum"
        ),
    },
    "while": {
        "title": "🔁 while sikli",
        "text": (
            "while — shart to'g'ri bo'lguncha takrorlanadi.\n\n"
            "```python\n"
            "son = 1\n"
            "while son <= 3:\n"
            "    print(son)\n"
            "    son += 1\n"
            "```\n\n"
            "Natija:\n"
            "1\n"
            "2\n"
            "3"
        ),
    },
    "list": {
        "title": "📋 Ro'yxatlar (list)",
        "text": (
            "list — bir nechta qiymatni bitta o'zgaruvchida saqlaydi.\n\n"
            "```python\n"
            "sonlar = [10, 20, 30]\n"
            "sonlar.append(40)\n"
            "print(sonlar)\n"
            "print(len(sonlar))\n"
            "print(sonlar[0])\n"
            "```\n\n"
            "Natija:\n"
            "[10, 20, 30, 40]\n"
            "4\n"
            "10"
        ),
    },
    "dict": {
        "title": "📖 Lug'at (dict)",
        "text": (
            "dict — kalit va qiymat juftliklarini saqlaydi.\n\n"
            "```python\n"
            "odam = {\"ism\": \"Aziz\", \"yosh\": 25}\n"
            "print(odam[\"ism\"])\n"
            "odam[\"shahar\"] = \"Toshkent\"\n"
            "print(odam)\n"
            "```\n\n"
            "Natija:\n"
            "Aziz\n"
            "{'ism': 'Aziz', 'yosh': 25, 'shahar': 'Toshkent'}"
        ),
    },
    "string": {
        "title": "🔤 Satr (string) funksiyalari",
        "text": (
            "Matnlar ustida ishlash uchun tayyor funksiyalar.\n\n"
            "```python\n"
            "matn = \"Salom Dunyo\"\n"
            "print(matn.upper())\n"
            "print(matn.lower())\n"
            "print(matn.split())\n"
            "print(len(matn))\n"
            "```\n\n"
            "Natija:\n"
            "SALOM DUNYO\n"
            "salom dunyo\n"
            "['Salom', 'Dunyo']\n"
            "11"
        ),
    },
    "math": {
        "title": "➗ Matematik funksiyalar",
        "text": (
            "Python'ning tayyor matematik funksiyalari.\n\n"
            "```python\n"
            "print(max(3, 7, 2))\n"
            "print(min(3, 7, 2))\n"
            "print(sum([1, 2, 3]))\n"
            "print(round(4.678, 1))\n"
            "print(abs(-5))\n"
            "```\n\n"
            "Natija:\n"
            "7\n"
            "2\n"
            "6\n"
            "4.7\n"
            "5"
        ),
    },
    "lambda": {
        "title": "⚡ Lambda (qisqa funksiya)",
        "text": (
            "lambda — bitta qatorli, nomsiz funksiya yaratadi.\n\n"
            "```python\n"
            "kvadrat = lambda x: x * x\n"
            "print(kvadrat(5))\n\n"
            "sonlar = [1, 2, 3, 4]\n"
            "juft = list(filter(lambda x: x % 2 == 0, sonlar))\n"
            "print(juft)\n"
            "```\n\n"
            "Natija:\n"
            "25\n"
            "[2, 4]"
        ),
    },
}


def build_menu() -> InlineKeyboardMarkup:
    """Mavzular menyusini yasaydi."""
    builder = InlineKeyboardBuilder()
    labels = {
        "print": "🖨 print()",
        "def": "🧩 def (funksiya)",
        "return": "↩️ return",
        "if": "🔀 if / elif / else",
        "for": "🔁 for sikli",
        "while": "🔁 while sikli",
        "list": "📋 list",
        "dict": "📖 dict",
        "string": "🔤 satrlar",
        "math": "➗ matematika",
        "lambda": "⚡ lambda",
    }
    for key, label in labels.items():
        builder.button(text=label, callback_data=f"lesson:{key}")
    builder.adjust(2)  # har qatorda 2 ta tugma
    return builder.as_markup()


# ------------------------------------------------------------
# Handlerlar
# ------------------------------------------------------------

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Men senga Python asoslarini amaliy misollar bilan o'rgataman.\n"
        "Quyidagi mavzulardan birini tanla:",
        reply_markup=build_menu(),
    )


@dp.message(F.text == "/menu")
async def menu_handler(message: types.Message):
    await message.answer("Mavzuni tanlang:", reply_markup=build_menu())


@dp.callback_query(F.data.startswith("lesson:"))
async def lesson_handler(callback: types.CallbackQuery):
    key = callback.data.split(":")[1]
    lesson = LESSONS.get(key)

    if lesson:
        text = f"*{lesson['title']}*\n\n{lesson['text']}"
        await callback.message.answer(text, parse_mode="Markdown")
    else:
        await callback.message.answer("Bu mavzu topilmadi.")

    await callback.answer()  # tugma bosilganini Telegram'ga bildiradi


# Foydalanuvchi oddiy matn yozsa
@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer(
        "Mavzular menyusini ko'rish uchun /menu buyrug'ini yuboring."
    )


# ------------------------------------------------------------
# Render "Web Service" bo'sh turmasligi uchun oddiy http server
# UptimeRobot aynan shu manzilga (/) so'rov yuborib botni uyg'oq tutadi
# ------------------------------------------------------------

async def health_check(request):
    return web.Response(text="Bot ishlayapti ✅")


async def on_startup(app):
    # Web-server ishga tushishi bilan bot pollingini orqa fonda boshlaymiz
    asyncio.create_task(dp.start_polling(bot))


def main():
    app = web.Application()
    app.router.add_get("/", health_check)
    app.on_startup.append(on_startup)

    port = int(os.getenv("PORT", 10000))  # Render shu orqali port beradi
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
