from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, WebAppInfo, InlineKeyboardButton
from db.models import Branche,session
from sqlalchemy import select

def phone_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Telefon number", request_contact=True),
    ])

    rkb.as_markup(resize_keyboard=True)
    return rkb.as_markup(resize_keyboard=True)


def menu_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Ofisga keldim"),
        KeyboardButton(text="Ofisdan ketdim"),
        KeyboardButton(text="Hisobotlar"),
    ])
    rkb.as_markup(resize_keyboard=True)
    rkb.adjust(1, 1,1)
    return rkb.as_markup(resize_keyboard=True)


def admin_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Yangi ishchi qo'shish"),
        KeyboardButton(text='Barcha ishchilar'),
        KeyboardButton(text='Barcha filiallar'),
        # KeyboardButton(text='Statistika 📊', web_app=WebAppInfo(url='#')),
    ])
    rkb.adjust(2, 1, 1)
    return rkb.as_markup(resize_keyboard=True)


def location_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Lokatsiya yuborish", request_location=True),
    ])
    rkb.as_markup(resize_keyboard=True)
    return rkb.as_markup(resize_keyboard=True)


def branches_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="fillial qo'shish"),
    ])
    result =session.execute(select(Branche.title))
    filiallar = [row[0] for row in result.all()]
    if filiallar:
        rkb.add(*[KeyboardButton(text=title) for title in filiallar])

    rkb.add(*[KeyboardButton(text="📁Bosh menuga qaytish")])
    rkb.adjust(1,repeat=True)
    return rkb.as_markup(resize_keyboard=True)

def employee_menu_button():
    ikb  = InlineKeyboardBuilder()
    ikb.add(*[
        InlineKeyboardButton(text="",data="")
    ])

def employee_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Ushbu ishchini o'chirish"),
        KeyboardButton(text="Ishchining hisobotini ko'rish"),
        KeyboardButton(text="📁 Bosh menuga qaytish"),
    ])
def moon_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Yanvar"),
        KeyboardButton(text="Fevral"),
        KeyboardButton(text="Mart"),
        KeyboardButton(text="Aprel"),
        KeyboardButton(text="May"),
        KeyboardButton(text="Iyun"),
        KeyboardButton(text="Iyul"),
        KeyboardButton(text="Avgust"),
        KeyboardButton(text="Sentabr"),
        KeyboardButton(text="Oktabr"),
        KeyboardButton(text="Noyabr"),
        KeyboardButton(text="Dekabr"),
    ])
    rkb.add(*[
        KeyboardButton(text="📁 Bosh menuga qaytish"),
    ])
    rkb.adjust(2,2,2,2,2,2,1)
    return rkb.as_markup(resize_keyboard=True)
def back_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text='🔙 Bekor qilish')
    ])
    return rkb.as_markup(resize_keyboard=True)

def branch_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Ushbu filialni o'chirib tashlash ❌"),
        KeyboardButton(text='🔙 Bekor qilish')
    ])
    rkb.adjust(1,1)
    return rkb.as_markup(resize_keyboard=True)

def delete_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Ha"),
        KeyboardButton(text="🔙 Bekor qilish")
    ])
    rkb.adjust(1,1)
    return rkb.as_markup(resize_keyboard=True)

