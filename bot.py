import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ChatMemberStatus

TOKEN = "BOT_TOKENINGIZNI_BU_YERGA_QO‘YING"
CHANNEL = "@Tarjimakodbot"
ADMIN_ID = 7431625430

bot = Bot(TOKEN)
dp = Dispatcher()

movies = {}
users = set()

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]
    except:
        return False

@dp.message(Command("start"))
async def start(msg: Message):
    users.add(msg.from_user.id)

    if not await check_sub(msg.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga azo bo‘lish", url="https://t.me/Tarjimakodbot")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")]
        ])
        await msg.answer(
            "❌ Botdan foydalanish uchun kanalga azo bo‘ling!",
            reply_markup=kb
        )
        return

    await msg.answer("🎬 Kino kodini yuboring\nMasalan: 125 yoki #125")

@dp.callback_query(F.data == "check")
async def recheck(call):
    if await check_sub(call.from_user.id):
        await call.message.answer("✅ Rahmat! Endi kino kodini yuboring")
    else:
        await call.answer("❌ Hali kanalga azo emassiz", show_alert=True)

@dp.message()
async def movie_handler(msg: Message):
    text = msg.text.replace("#", "")
    if text.isdigit():
        code = int(text)
        if code in movies:
            await bot.copy_message(
                chat_id=msg.chat.id,
                from_chat_id=CHANNEL,
                message_id=movies[code]
            )

@dp.message(Command("admin"))
async def admin(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    await msg.answer(
        "🛠 ADMIN PANEL\n\n"
        "/add kod (reply kino)\n"
        "/del kod\n"
        "/stat"
    )

@dp.message(Command("add"))
async def add_movie(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    if not msg.reply_to_message:
        await msg.answer("❌ Kinoga reply qiling")
        return

    code = int(msg.text.split()[1])
    movies[code] = msg.reply_to_message.message_id
    await msg.answer(f"✅ Kino qo‘shildi: {code}")

@dp.message(Command("del"))
async def del_movie(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        return
    code = int(msg.text.split()[1])
    movies.pop(code, None)
    await msg.answer("🗑 Kino o‘chirildi")

@dp.message(Command("stat"))
async def stat(msg: Message):
    if msg.from_user.id == ADMIN_ID:
        await msg.answer(f"👥 Foydalanuvchilar soni: {len(users)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
