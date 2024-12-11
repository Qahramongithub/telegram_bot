from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import insert, select, update
import math

from bot.button.button import menu_button, back_button, moon_button
from bot.state import EmployeesState
from db.models import session, User, Att, Login, Branche

employees_router = Router()
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius = 6371000  # Yer radiusi (metrda)

    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)

    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad

    a = sin(d_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius * c


@employees_router.message(EmployeesState.start_work, F.text == "🔙 Bekor qilish")
@employees_router.message(EmployeesState.employees)
async def employees(message: Message, state: FSMContext):
    try:
        if message.contact:
            await state.update_data({"phone": message.contact.phone_number})
        else:
            pass
        data = await state.get_data()
        # user_query = select(User.id).where(User.phone_number == data['phone'])
        # user = session.execute(user_query)
        # if user.exists():
        #     await message.answer("Siz tizimga muvaffaqqiyatli kirdingiz", reply_markup=menu_button())
        # else:
        #     await message.answer("Hodim topilmadi")
        await message.answer("status kod kiriting")
        await state.set_state(EmployeesState.status)
    except Exception as e:
        pass


@employees_router.message(EmployeesState.status)
@employees_router.message(EmployeesState.office, F.text == "🔙 Bekor qilish")
async def employees(message: Message, state: FSMContext):
    try:
        status = message.text
        data = await state.get_data()
        result = session.execute(select(Login.admin_id))
        status1 = [row[0] for row in result.all()]
        for i in status1:
            if i == status:
                await state.update_data({"status": i})
                await message.answer("Siz tizimga muvaffaqiyatli kirdingiz", reply_markup=menu_button())
                await state.set_state(EmployeesState.office)
    except Exception as e:
        pass


@employees_router.message(EmployeesState.office, F.text == "Ofisga keldim")
async def employees(message: Message, state: FSMContext):
    await message.answer("Iltimos , live lokatsiya yuboring")
    await state.set_state(EmployeesState.employee_location)


@employees_router.message(EmployeesState.employee_location, F.location)
async def employees(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        print("true")
        await state.update_data({'longitude': message.location.longitude})
        await state.update_data({'latitude': message.location.latitude})
        lon1 = message.location.longitude
        lat1 = message.location.latitude
        user = session.execute(select(User.id).where(User.phone_number == data['phone'])).scalars().first()
        date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        start_at = f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        date_time =f"{date} {start_at}"
        if message.location.live_period:
            if user:
                s = False
                results = session.execute(select(Branche.longitude, Branche.latitude, Branche.radius)).all()

                for lon, lat, r in results:
                    if calculate_distance(lon, lat, lon1, lat1) < r:
                        s = True
                        session.execute(insert(Att).values(
                            time=start_at, date=date, user_id=user,
                            staff=data['name'],
                            date_time =date_time,
                            status=data['status']
                        ))
                        session.commit()
                        break

                if s == False:
                    await message.answer("Ishxonaga yaqinroq keling !", reply_markup=menu_button())
                    await state.set_state(EmployeesState.office)


                else:
                    await message.answer("Ishingizga omad", reply_markup=menu_button())
                    await state.set_state(EmployeesState.office)




            else:
                await message.answer("hodim topilmadi !")

        else:
            await message.answer("live lokatsiya kiriting !")
    except Exception as e:
        pass


@employees_router.message(EmployeesState.office, F.text == "Ofisdan ketdim")
async def employees(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        date = f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}"
        start_at = f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        user = session.execute(select(User.id).where(User.phone_number == data['phone'])).scalars().first()
        datatime = f"{date} {start_at}"
        if date and user:
            session.execute(
                insert(Att).values(date=date, user_id=user, date_time=datatime, time=start_at, status=data['status'],
                                   staff=data['name']))
            session.commit()
            await message.answer("yaxshi dam oling")
            await state.set_state(EmployeesState.start_work)


        else:
            await message.answer("Siz bugun ishga kelmagansiz")
    except Exception as e:
        pass

#
# @employees_router.message(EmployeesState.office, F.text == "Hisobotlar")
# async def employees(message: Message, state: FSMContext):
#     await message.answer("Oylik hisobotni ko'rish", reply_markup=moon_button())
#     await state.set_state(EmployeesState.report)
