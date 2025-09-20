import os
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.filters import Command

welcome_router = Router()

welcome_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔎 Найти работу", callback_data="seeker_menu")],
        [InlineKeyboardButton(text="🧑‍💼 Найти сотрудника", callback_data="employer_menu")]
    ]
)

WELCOME_TEXT = (
    "👋 <b>Добро пожаловать в DevConnect!</b>\n\n"
    "🚀 <i>Современная платформа для поиска работы в IT</i>\n\n"
    "<b>✨ Возможности бота:</b>\n"
    "• 📝 Создание и редактирование резюме/вакансий\n"
    "• 👀 Просмотр предложений с красивым интерфейсом\n"
    "• 🎯 Поиск подходящих кандидатов и вакансий\n"
    "• 💬 Прямая связь между работодателями и соискателями\n\n"
    "🎯 <b>Выберите роль:</b>"
)

WELCOME_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "welcome.png")

@welcome_router.message(Command("start"))
async def send_welcome(message: Message):
    if os.path.exists(WELCOME_IMAGE_PATH):
        photo = FSInputFile(WELCOME_IMAGE_PATH)
        await message.answer_photo(photo, caption=WELCOME_TEXT, reply_markup=welcome_kb, parse_mode="HTML")
    else:
        await message.answer(WELCOME_TEXT, reply_markup=welcome_kb, parse_mode="HTML")

@welcome_router.callback_query(F.data == "seeker_menu")
async def seeker_menu_callback(callback: CallbackQuery):
    await callback.message.delete()
    from handlers.seeker import SEEKER_MENU_TEXT, seeker_menu_kb
    await callback.message.answer(SEEKER_MENU_TEXT, reply_markup=seeker_menu_kb, parse_mode="HTML")

@welcome_router.callback_query(F.data == "employer_menu")
async def employer_menu_callback(callback: CallbackQuery):
    await callback.message.delete()
    from handlers.employer import EMPLOYER_MENU_TEXT, employer_menu_kb
    await callback.message.answer(EMPLOYER_MENU_TEXT, reply_markup=employer_menu_kb, parse_mode="HTML")
