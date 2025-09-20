from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import get_resume, create_resume, delete_resume, get_vacancies

seeker_router = Router()

seeker_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать резюме", callback_data="create_resume")],
        [InlineKeyboardButton(text="📋 Просмотр вакансий", callback_data="view_vacancies")],
        [InlineKeyboardButton(text="👤 Моя анкета", callback_data="my_resume")],
        [InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_welcome")]
    ]
)

SEEKER_MENU_TEXT = (
    "👤 <b>Меню соискателя</b>\n\n"
    "Выберите действие:\n\n"
    "📝 <i>Создать резюме</i>\n"
    "📋 <i>Просмотр вакансий</i>\n"
    "👤 <i>Моя анкета</i>\n"
    "🔙 <i>Вернуться в главное меню</i>"
)

class ResumeForm(StatesGroup):
    name = State()
    specialization = State()
    experience = State()
    skills = State()
    contacts = State()

@seeker_router.message(F.text == "🔎 Найти работу")
async def seeker_menu(message: Message):
    await message.answer(SEEKER_MENU_TEXT, reply_markup=seeker_menu_kb, parse_mode="HTML")

@seeker_router.callback_query(F.data == "create_resume")
async def create_resume_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = callback.from_user.id
    resume = get_resume(user_id)
    if resume:
        msg = await callback.message.answer(
            "⚠️ <b>У вас уже есть резюме!</b>\n\n"
            "Хотите отредактировать его?\n"
            "📝 <i>Отправьте 'Редактировать резюме'</i>\n"
            "🗑️ <i>Для удаления — 'Удалить резюме'</i>",
            reply_markup=seeker_menu_kb,
            parse_mode="HTML"
        )
        await state.update_data(last_bot_message_id=msg.message_id)
        return

    msg = await callback.message.answer("👤 <b>Создание резюме</b>\n\n📝 Введите ваше имя:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.name)

@seeker_router.message(ResumeForm.name)
async def resume_name(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(name=message.text)
    msg = await message.answer("👤 <b>Создание резюме</b>\n\n🎯 Введите вашу специализацию:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.specialization)

@seeker_router.message(ResumeForm.specialization)
async def resume_specialization(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(specialization=message.text)
    msg = await message.answer("👤 <b>Создание резюме</b>\n\n💼 Укажите ваш опыт работы:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.experience)

@seeker_router.message(ResumeForm.experience)
async def resume_experience(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(experience=message.text)
    msg = await message.answer("👤 <b>Создание резюме</b>\n\n🛠️ Укажите ваши ключевые навыки:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.skills)

@seeker_router.message(ResumeForm.skills)
async def resume_skills(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(skills=message.text)
    msg = await message.answer("👤 <b>Создание резюме</b>\n\n📞 Укажите ваши контактные данные:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.contacts)

@seeker_router.message(ResumeForm.contacts)
async def resume_contacts(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    user_id = message.from_user.id
    create_resume(
        user_id,
        data["name"],
        data["specialization"],
        data["experience"],
        data["skills"],
        message.text
    )
    await message.answer("✅ <b>Резюме успешно создано!</b>\n\n👤 Теперь вы можете просматривать вакансии.", reply_markup=seeker_menu_kb, parse_mode="HTML")
    await state.clear()

@seeker_router.callback_query(F.data == "my_resume")
async def my_resume_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = callback.from_user.id
    resume = get_resume(user_id)
    if not resume:
        msg = await callback.message.answer(
            "📋 <b>Ваша анкета</b>\n\n"
            "❌ У вас нет созданного резюме.\n\n"
            "📝 <i>Создайте резюме через меню</i>",
            reply_markup=seeker_menu_kb,
            parse_mode="HTML"
        )
        await state.update_data(last_bot_message_id=msg.message_id)
        return

    msg = await callback.message.answer(
        "📋 <b>Ваше резюме</b>\n\n"
        f"👨‍💼 <b>Имя:</b> {resume[1]}\n"
        f"🎯 <b>Специализация:</b> {resume[2]}\n"
        f"💼 <b>Опыт работы:</b> {resume[3]}\n"
        f"🛠️ <b>Навыки:</b> {resume[4]}\n"
        f"📞 <b>Контакты:</b> {resume[5]}\n\n"
        "📝 <i>Для редактирования — отправьте 'Редактировать резюме'</i>\n"
        "🗑️ <i>Для удаления — 'Удалить резюме'</i>",
        reply_markup=seeker_menu_kb,
        parse_mode="HTML"
    )
    await state.update_data(last_bot_message_id=msg.message_id)

@seeker_router.message(F.text == "Редактировать резюме")
async def edit_resume(message: Message, state: FSMContext):
    await message.delete()
    user_id = message.from_user.id
    resume = get_resume(user_id)
    if not resume:
        msg = await message.answer("❌ У вас нет резюме для редактирования.", reply_markup=seeker_menu_kb, parse_mode="HTML")
        await state.update_data(last_bot_message_id=msg.message_id)
        return
    msg = await message.answer("👤 <b>Редактирование резюме</b>\n\n📝 Введите новое имя (или отправьте текущее):")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(ResumeForm.name)

@seeker_router.callback_query(F.data == "view_vacancies")
async def view_vacancies_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(vacancy_page=0)
    await send_vacancy_page(callback.message, state)

async def send_vacancy_page(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("vacancy_page", 0)
    limit = 1
    offset = page * limit
    vacancies = get_vacancies(offset=offset, limit=limit)
    if not vacancies:
        await message.answer(
            "📋 <b>Вакансии не найдены</b>\n\n"
            "К сожалению, в базе данных нет доступных вакансий.",
            reply_markup=seeker_menu_kb,
            parse_mode="HTML"
        )
        return

    vacancy = vacancies[0]

    navigation_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_vacancy"),
                InlineKeyboardButton(text="➡️ Далее", callback_data="next_vacancy")
            ],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_welcome")]
        ]
    )

    await message.answer_photo(
        photo=FSInputFile("assets/vacancy.png"),
        caption=f"💼 <b>Вакансия #{page + 1}</b>\n\n"
               f"🏢 <b>Название компании:</b> {vacancy[2]}\n"
               f"👔 <b>Вакантная позиция:</b> {vacancy[3]}\n"
               f"📋 <b>Описание:</b> {vacancy[4]}\n"
               f"📋 <b>Условия:</b> {vacancy[5]}\n"
               f"📞 <b>Контакты:</b> {vacancy[6]}",
        parse_mode="HTML",
        reply_markup=navigation_kb
    )

@seeker_router.callback_query(F.data == "next_vacancy")
async def next_vacancy_page(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    page = data.get("vacancy_page", 0) + 1
    await state.update_data(vacancy_page=page)
    await send_vacancy_page(callback.message, state)

@seeker_router.callback_query(F.data == "prev_vacancy")
async def prev_vacancy_page(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    page = max(data.get("vacancy_page", 0) - 1, 0)
    await state.update_data(vacancy_page=page)
    await send_vacancy_page(callback.message, state)

@seeker_router.message(F.text == "Удалить резюме")
async def delete_my_resume(message: Message, state: FSMContext):
    await message.delete()

    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass

    user_id = message.from_user.id
    delete_resume(user_id)
    from handlers.welcome import WELCOME_TEXT, welcome_kb
    await message.answer("✅ <b>Резюме успешно удалено!</b>\n\n🏠 Возвращаемся к главному меню...", reply_markup=welcome_kb, parse_mode="HTML")

@seeker_router.callback_query(F.data == "back_to_welcome")
async def back_to_welcome_callback(callback: CallbackQuery):
    await callback.message.delete()
    from handlers.welcome import WELCOME_TEXT, welcome_kb
    await callback.message.answer(WELCOME_TEXT, reply_markup=welcome_kb, parse_mode="HTML")
