from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from db.models import Branche, session, User
from sqlalchemy import select, delete, insert
from bot.button.button import admin_button, branches_button, back_button, branch_button, delete_button
from bot.state import DirectorsState
import re

director_router = Router()


@director_router.message(DirectorsState.location, F.text == "🔙 Bekor qilish")
@director_router.message(DirectorsState.new_location, F.text == "🔙 Bekor qilish")
@director_router.message(DirectorsState.new_branch, F.text == "📁Bosh menuga qaytish")
@director_router.message(DirectorsState.location, F.text == "🔙 Bekor qilish")
@director_router.message(DirectorsState.branch_delete, F.text == "🔙 Bekor qilish")
@director_router.message(DirectorsState.delete, F.text == "🔙 Bekor qilish")
@director_router.message(DirectorsState.branches, F.text == '📁Bosh menuga qaytish')
@director_router.message(DirectorsState.directors,F.contact)
async def director(message: Message, state: FSMContext):
    try:
        await message.answer("Menu ", reply_markup=admin_button())
        # user_query = select(User.id).where(User.phone_number == data['phone'])
        # user = session.execute(user_query)
        # if user.exists():
        #     await message.answer("Menu ",reply_markup=admin_button())
        # else:
        #     await message.answer("Hodim topilmadi")
        await state.set_state(DirectorsState.director_menu)
    except Exception as e:
        pass


@director_router.message(DirectorsState.director_menu, F.text == "Yangi ishchi qo'shish")
async def director(message: Message, state: FSMContext):
    try:
        await message.answer("Yangi ishchi ism ")
        await state.set_state(DirectorsState.name)
    except Exception as e:
        pass


# @director_router.message(DirectorsState.name)
# async def director(message: Message, state: FSMContext):
#     try:
#         await state.update_data({"name": message.text})
#         await message.answer("Yishchi oylik haqi kiritilsin !")
#         await state.set_state(DirectorsState.price)
#     except Exception as e:
#         pass

@director_router.message(DirectorsState.name)
async def director_name_handler(message: Message, state: FSMContext):
    try:
        price = message.text

        # Foydalanuvchidan ismni saqlash
        # await state.update_data({"price": message.text})
        await state.update_data({"name": message.text})

        await message.answer("Yangi ishchi telefon raqamini kiriting\nMasalan: 998(94)5421234")
        await state.set_state(DirectorsState.phone)
    # else:
    #     await message.answer("narx raqamlarda kiritilsin !")
    #     await state.set_state(DirectorsState.price)

    except Exception as e:
        pass


@director_router.message(DirectorsState.phone)
async def director_phone_handler(message: Message, state: FSMContext):
    try:
        phone = message.text
        data = await state.get_data()

        # Telefon raqamni regex yordamida tekshirish
        if re.fullmatch(r"998\d{9}", phone):
            try:
                # Ma'lumotni bazaga yozish
                session.execute(insert(User).values(phone_number=phone, staff=data['name']))
                session.commit()

                await message.answer("Yangi ishchi qo'shildi", reply_markup=admin_button())
                await state.clear()
                await state.set_state(DirectorsState.director_menu)
            except Exception as e:
                await message.answer(f"Xatolik yuz berdi: {e}")
        else:
            # Agar telefon raqam noto‘g‘ri formatda bo‘lsa
            await message.answer("Telefon raqam noto‘g‘ri formatda. Qayta kiriting: 998XXXXXXXXX")
    except Exception as e:
        pass


@director_router.message(DirectorsState.new_branch)
@director_router.message(DirectorsState.director_menu, F.text == "Barcha filiallar")
async def director_menu(message: Message, state: FSMContext):
    try:
        await message.answer("Menu ", reply_markup=branches_button())
        await state.set_state(DirectorsState.branches)
    except Exception as e:
        pass


@director_router.message(DirectorsState.branches, F.text == "fillial qo'shish")
async def director_menu(message: Message, state: FSMContext):
    try:
        await message.answer('Yangi filiallning qisqacha nomini kiriting', reply_markup=back_button())
        await state.set_state(DirectorsState.location)
    except Exception as e:
        pass


@director_router.message(DirectorsState.location)
async def director_menu(message: Message, state: FSMContext):
    try:
        if message.text == "fillial qo'shish" or message.text == "🔙 Bekor qilish":
            await message.answer("Boshqa filial nomidan foydalaning !")
            await state.set_state(DirectorsState.location)

        else:
            await state.update_data({'name': message.text})
            await message.answer('Yangi filiallning lokatsiyasini kiriting', reply_markup=back_button())
            await state.set_state(DirectorsState.new_location)
    except Exception as e:
        pass


@director_router.message(DirectorsState.new_location, F.location)
async def director_menu(message: Message, state: FSMContext):
    try:
        await state.update_data({'longitude': message.location.longitude})
        await state.update_data({'latitude': message.location.latitude})
        await message.answer('Ishxona radiusini kiriting\nFaqat raqamlardan foydalaning')
        await state.set_state(DirectorsState.radius)
    except Exception as e:
        pass


@director_router.message(DirectorsState.radius)
async def director_menu(message: Message, state: FSMContext):
    try:
        radius = message.text
        data = await state.get_data()
        if radius.isdigit():
            session.execute(insert(Branche).values(
                title=data['name'], longitude=data['longitude'], latitude=data['latitude'], radius=radius)
            )
            session.commit()
            await message.answer("Yangi filial muvaffaqqiyatli qo'shildi", reply_markup=branches_button())
            await state.set_state(DirectorsState.new_branch)
        else:
            await message.answer("Faqat raqamlardan foydalaning !")
            await state.set_state(DirectorsState.radius)
    except Exception as e:
        pass


@director_router.message(DirectorsState.branches)
async def director_menu(message: Message, state: FSMContext):
    try:
        branch = message.text
        result = session.execute(select(Branche.title))
        filiallar = [row[0] for row in result.all()]
        for filial in filiallar:
            if filial in branch:
                await message.answer(f"Siz tanlagan filial nomi: {branch}", reply_markup=branch_button())
                await state.update_data({"branch": branch})
                await state.set_state(DirectorsState.branch_delete)
    except Exception as e:
        pass


@director_router.message(DirectorsState.branch_delete, F.text == "Ushbu filialni o'chirib tashlash ❌")
async def director_menu(message: Message, state: FSMContext):
    await message.answer("Ushbu filialni o'chirmoqchimisiz ?", reply_markup=delete_button())
    await state.set_state(DirectorsState.delete)


@director_router.message(DirectorsState.delete, F.text == "Ha")
async def branch_delete(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        branch = data['branch']
        try:
            branch_search = session.query(Branche).filter(Branche.title == branch).first()
            if not branch_search:
                await message.answer(f"No branch found with the title '{branch}'.")
                return
            session.execute(delete(Branche).where(Branche.title == branch))
            session.commit()
            await message.answer(f"Filial '{branch}' o'chirildi.")
        except Exception as e:
            pass

    except Exception as e:
        session.rollback()
        await message.answer("Error")
