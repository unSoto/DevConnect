from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db import get_vacancy_by_user, create_vacancy, delete_vacancy, get_resumes_excluding_user

employer_router = Router()

employer_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Создать вакансию", callback_data="create_vacancy")],
        [InlineKeyboardButton(text="👥 Просмотр резюме", callback_data="view_resumes")],
        [InlineKeyboardButton(text="🏢 Моя анкета", callback_data="my_profile")],
        [InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_welcome")]
    ]
)

EMPLOYER_MENU_TEXT = (
    "🏢 <b>Меню работодателя</b>\n\n"
    "Выберите действие:\n\n"
    "📝 <i>Создать вакансию</i>\n"
    "👥 <i>Просмотр резюме</i>\n"
    "🏢 <i>Моя анкета</i>\n"
    "🔙 <i>Вернуться в главное меню</i>"
)

class VacancyForm(StatesGroup):
    company_name = State()
    position = State()
    requirements = State()
    conditions = State()
    contacts = State()

@employer_router.message(F.text == "🧑‍💼 Найти сотрудника")
async def employer_menu(message: Message):
    await message.answer(EMPLOYER_MENU_TEXT, reply_markup=employer_menu_kb, parse_mode="HTML")

@employer_router.callback_query(F.data == "create_vacancy")
async def create_vacancy_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = callback.from_user.id
    vacancy = get_vacancy_by_user(user_id)
    if vacancy:
        msg = await callback.message.answer(
            "⚠️ <b>У вас уже есть вакансия!</b>\n\n"
            "Хотите отредактировать её?\n"
            "📝 <i>Отправьте 'Редактировать вакансию'</i>\n"
            "🗑️ <i>Для удаления — 'Удалить вакансию'</i>",
            reply_markup=employer_menu_kb,
            parse_mode="HTML"
        )
        await state.update_data(last_bot_message_id=msg.message_id)
        return

    msg = await callback.message.answer("🏢 <b>Создание вакансии</b>\n\n📝 Введите название компании:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.company_name)

@employer_router.message(VacancyForm.company_name)
async def vacancy_company_name(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(company_name=message.text)
    msg = await message.answer("📝 <b>Создание вакансии</b>\n\n👔 Введите название должности:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.position)

@employer_router.message(VacancyForm.position)
async def vacancy_position(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(position=message.text)
    msg = await message.answer("📝 <b>Создание вакансии</b>\n\n📋 Опишите требования к кандидату:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.requirements)

@employer_router.message(VacancyForm.requirements)
async def vacancy_requirements(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(requirements=message.text)
    msg = await message.answer("📝 <b>Создание вакансии</b>\n\n💰 Опишите условия работы (зарплата, график, льготы и т.д.):")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.conditions)

@employer_router.message(VacancyForm.conditions)
async def vacancy_conditions(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    await state.update_data(conditions=message.text)
    msg = await message.answer("📝 <b>Создание вакансии</b>\n\n📞 Укажите контактные данные для связи:")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.contacts)

@employer_router.message(VacancyForm.contacts)
async def vacancy_contacts(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    last_bot_msg_id = data.get("last_bot_message_id")
    if last_bot_msg_id:
        try:
            await message.bot.delete_message(message.chat.id, last_bot_msg_id)
        except:
            pass

    user_id = message.from_user.id
    create_vacancy(
        user_id,
        data["company_name"],
        data["position"],
        data["requirements"],
        data["conditions"],
        message.text
    )
    await message.answer("✅ <b>Вакансия успешно создана!</b>\n\n🏢 Теперь вы можете просматривать резюме кандидатов.", reply_markup=employer_menu_kb, parse_mode="HTML")
    await state.clear()

@employer_router.callback_query(F.data == "my_profile")
async def my_profile_callback(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id
    vacancy = get_vacancy_by_user(user_id)
    if not vacancy:
        await callback.message.answer(
            "📋 <b>Ваша анкета</b>\n\n"
            "❌ У вас нет созданной вакансии.\n\n"
            "📝 <i>Создайте вакансию через меню</i>",
            reply_markup=employer_menu_kb,
            parse_mode="HTML"
        )
        return

    await callback.message.answer(
        "📋 <b>Ваша вакансия</b>\n\n"
        f"🏢 <b>Компания:</b> {vacancy[2]}\n"
        f"👔 <b>Должность:</b> {vacancy[3]}\n"
        f"📋 <b>Требования:</b> {vacancy[4]}\n"
        f"💰 <b>Условия:</b> {vacancy[5]}\n"
        f"📞 <b>Контакты:</b> {vacancy[6]}\n\n"
        "📝 <i>Для редактирования — отправьте 'Редактировать вакансию'</i>\n"
        "🗑️ <i>Для удаления — 'Удалить вакансию'</i>",
        reply_markup=employer_menu_kb,
        parse_mode="HTML"
    )

@employer_router.message(F.text == "Редактировать вакансию")
async def edit_vacancy(message: Message, state: FSMContext):
    await message.delete()
    user_id = message.from_user.id
    vacancy = get_vacancy_by_user(user_id)
    if not vacancy:
        msg = await message.answer("❌ У вас нет вакансии для редактирования.", reply_markup=employer_menu_kb, parse_mode="HTML")
        await state.update_data(last_bot_message_id=msg.message_id)
        return
    msg = await message.answer("🏢 <b>Редактирование вакансии</b>\n\n📝 Введите новое название компании (или отправьте текущее):")
    await state.update_data(last_bot_message_id=msg.message_id)
    await state.set_state(VacancyForm.company_name)

@employer_router.callback_query(F.data == "view_resumes")
async def view_resumes_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(resume_page=0)
    await send_resume_page(callback.message, state)

async def send_resume_page(message: Message, state: FSMContext):
    data = await state.get_data()
    page = data.get("resume_page", 0)
    limit = 1
    offset = page * limit
    user_id = message.from_user.id
    resumes = get_resumes_excluding_user(user_id, offset=offset, limit=limit)

    if not resumes:
        if page == 0:
            await message.answer(
                "📋 <b>Резюме не найдены</b>\n\n"
                "К сожалению, в базе данных нет доступных резюме.",
                reply_markup=employer_menu_kb,
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "📋 <b>Конец списка</b>\n\n"
                "Больше резюме нет в базе данных.",
                reply_markup=employer_menu_kb,
                parse_mode="HTML"
            )
        return

    resume = resumes[0]

    navigation_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_resume"),
                InlineKeyboardButton(text="➡️ Далее", callback_data="next_resume")
            ],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_welcome")]
        ]
    )

    await message.answer_photo(
        photo=FSInputFile("assets/resume.png"),
        caption=f"👤 <b>Резюме #{page + 1}</b>\n\n"
               f"👨‍💼 <b>Специалист:</b> {resume[1]}\n"
               f"🎯 <i>Специализация:</i> {resume[2]}\n"
               f"💼 <i>Опыт работы:</i> {resume[3]}\n"
               f"🛠️ <i>Навыки:</i> {resume[4]}\n"
               f"📞 <i>Контакты:</i> {resume[5]}",
        parse_mode="HTML",
        reply_markup=navigation_kb
    )

@employer_router.callback_query(F.data == "next_resume")
async def next_resume_page(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    page = data.get("resume_page", 0) + 1
    await state.update_data(resume_page=page)
    await send_resume_page(callback.message, state)

@employer_router.callback_query(F.data == "prev_resume")
async def prev_resume_page(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    page = max(data.get("resume_page", 0) - 1, 0)
    await state.update_data(resume_page=page)
    await send_resume_page(callback.message, state)

@employer_router.message(F.text == "Удалить вакансию")
async def delete_my_vacancy(message: Message, state: FSMContext):
    await message.delete()

    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass

    user_id = message.from_user.id
    delete_vacancy(user_id)
    from handlers.welcome import WELCOME_TEXT, welcome_kb
    await message.answer("✅ <b>Вакансия успешно удалена!</b>\n\n🏠 Возвращаемся к главному меню...", reply_markup=welcome_kb, parse_mode="HTML")

@employer_router.callback_query(F.data == "back_to_welcome")
async def back_to_welcome_callback(callback: CallbackQuery):
    await callback.message.delete()
    from handlers.welcome import WELCOME_TEXT, welcome_kb
    await callback.message.answer(WELCOME_TEXT, reply_markup=welcome_kb, parse_mode="HTML")
