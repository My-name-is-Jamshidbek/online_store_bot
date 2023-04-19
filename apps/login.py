"""
log in
"""
from aiogram.types import Message as m
from aiogram.dispatcher import FSMContext as s

from buttons.inlinekeyboardbuttons import inlinekeyboardbutton
from buttons.keyboardbuttons import keyboardbutton
from config import menus
from database.database import is_admin, is_supadmin, create_database, add_admin, add_category, get_user_by_tg_ids as \
    get_user_by_tg_id, \
    add_new_user
# from database.database import *
from states import *


async def cmd_start(m: m):
    """
    :param m:
    :return:
    """

    # create_database()
    # add_admin(ism="Jam1", familiya='O1', telefon="+9981", aloqa='t.me/mal_un', tg_id='2081653869')
    # add_category('cat1')
    # add_category('cat2')
    # add_category('cat3')
    # add_product(
    #     name='p2',
    #     category_id=1,
    #     about="lkm",
    #     price=456,
    #     photo='nk',
    # )
    if is_admin(m.chat.id):
        await m.answer(
            "Assalomu aleykum admin\nBotga hush kelibsiz\nKerakli menyuni tanlashiniz mumkin.",
            reply_markup=keyboardbutton(list(menus['admin'][0].keys()), row=2)
        )
        await Admin_state.main_menu.set()
    elif is_supadmin(m.chat.id):
        await m.answer(
            "Assalomu aleykum supadmin\nBotga hush kelibsiz\nKerakli menyuni tanlashiniz mumkin.",
            reply_markup=keyboardbutton(list(menus['supadmin'][0].keys()), row=2)
        )
        await Supadmin_state.main_menu.set()
    else:
        await m.answer("Assalomu aleykum\nBotga hush kelibsiz!\nSiz muvaffaqiyatli ro'yxatdan o'tdingiz malumotlaringizni \"Mening malumotlarim\" menyusidan o'zgartirishingiz mumkin.",
                       reply_markup=keyboardbutton(
            btns=list(menus[
            'user'][0].keys())))
        if not get_user_by_tg_id(m.chat.id):
            add_user = add_new_user(
                name=m.chat.full_name,
                phone_number="Kiritilmagan",
                aloqa="Kiritilmagan",
                viloyat="Kiritilmagan",
                tuman="kiritilmagan",
                address="Kiritilmagan",
                tg_id=m.chat.id
            )
        await User_state.main_menu.set()
