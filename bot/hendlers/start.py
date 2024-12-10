from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.button.button import phone_button
from bot.state import UserState, EmployeesState, DirectorsState

start_router = Router()


@start_router.message(CommandStart())
async def start_bot(message: Message, state: FSMContext):
    qr_id = message.text.split()[-1]
    await state.update_data({'role': qr_id})
    await message.answer("Assalomu aleykum !\n"
                         "Botimizga xush kelibsiz.\n"
                         "Iltimos, ismingizni lotin harflarida kiriting")
    await state.set_state(UserState.name)


@start_router.message(UserState.name)
async def name_bot_func(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})
    await message.answer("📞 Biz siz bilan bog'lanish imkoniga ega bo'lishimiz "
                         "uchun raqamingizni pastdagi tugma orqali yuboring", reply_markup=phone_button())
    data = await state.get_data()

    if data['role'] in 'admin':
        await state.set_state(DirectorsState.directors)
    elif data['role'] in 'employees':
        await state.set_state(EmployeesState.employees)
    else:
        await message.answer("Error")

