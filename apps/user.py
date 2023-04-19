"""
user
"""
from aiogram.types import Message as m, InputFile, CallbackQuery, InlineQuery, callback_query
from aiogram.dispatcher import FSMContext as s, FSMContext

from buttons.inlinekeyboardbuttons import inlinekeyboardbutton
from buttons.keyboardbuttons import keyboardbutton
from config import menus
from database.database import categories, products, product, get_user_by_tg_id, add_order, get_product_id, \
    change_user_data, get_orders_by_user_tg_id, get_product_all_data_by_id
from loader import bot
from states import User_state


async def user_main_menu(m: m, state: s):
    if m.text == "Mahsulotlar":
        categories_ = categories()
        if categories_:
            categories_.append("Chiqish")
        else:
            categories_ = ["Chiqish"]
        await m.answer(
            text='Mahsulot turini tanlang:',
            reply_markup=keyboardbutton(categories_)
        )
        await User_state.categories.set()
    elif m.text == "Buyurtmalarim":
        database = get_orders_by_user_tg_id(m.chat.id)
        for data in database:
            product_data = get_product_all_data_by_id(data[1])
            try:
                if product_data[3][-4:] == ".jpg":
                    photo = InputFile(product_data[3])
                elif product_data[3][-4:] == ".mp4":
                    video = InputFile(product_data[3])
                else:
                    photo, video = False, False
            except Exception as _:
                photo, video = False, False
            caption = f"{product_data[0]}\n" \
                      f"{product_data[1]}\n" \
                      f"{product_data[2]}\n" \
                      f"Buyurtma soni: {data[2]}"
            if photo:
                await m.answer_photo(photo=photo, caption=caption)
            elif video:
                await m.answer_video(video=video, caption=caption)
            else:
                await m.answer(text=caption)
    elif m.text == "Mening ma'lumotlarim":
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash", "O'zgartirish"], row=2))
        await User_state.change_data_personal.set()

async def change_data_personal(m: m, state: s):
    if m.text == "O'zgartirish":
        await m.answer("O'zgartirmoqchi bo'lgan malumotingizni tanlang:", reply_markup=keyboardbutton(["F.I",
                                                                                                       "Telefon",
                                                                                                       "Aloqa",
                                                                                                       "Viloyat",
                                                                                                       "Tuman",
                                                                                                       "Manzil",
                                                                                                       "Bekor "
                                                                                                       "qilish"],
                                                                                                      row=2))
        await User_state.change_data_personal_.set()
    elif m.text == "Tasdiqlash":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()


async def change_data_personal_(m: m, state: s):
    if m.text == "Bekor qilish":
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlarni o'zgartirish bekor qilindi. Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash",
                                                    "O'zgartirish"], row=2))
        await User_state.change_data_personal.set()

    elif m.text in ("F.I", "Telefon", "Aloqa", 'Viloyat', "Tuman", "Manzil"):
        await m.answer("Yangi malumotni kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await state.update_data(change_about=m.text)
        await User_state.change_data_personal_acces.set()


async def change_data_personal_acces(m: m, state: s):
    if m.text == "Bekor qilish":
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlarni o'zgartirish bekor qilindi. Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash",
                                                    "O'zgartirish"], row=2))
        await User_state.change_data_personal.set()

    data = await state.get_data()
    change_about = data.get("change_about")
    uid = get_user_by_tg_id(tg_id=m.from_user.id)["id"]
    re = False
    if change_about == "F.I":
        if change_user_data(user_id=uid, name=m.text):
            re = True
    elif change_about == "Telefon":
        if change_user_data(user_id=uid, phone_number=m.text):
            re = True
    elif change_about == "Aloqa":
        if change_user_data(user_id=uid, aloqa=m.text):
            re = True
    elif change_about == "Viloyat":
        if change_user_data(user_id=uid, viloyat=m.text):
            re = True
    elif change_about == "Tuman":
        if change_user_data(user_id=uid, tuman=m.text):
            re = True
    elif change_about == "Manzil":
        if change_user_data(user_id=uid, address=m.text):
            re = True

    if re:
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash", "O'zgartirish"], row=2))
        await User_state.change_data_personal.set()


async def user_categories_f(m: m, state: s):
    text = m.text
    if text == "Chiqish":
        await m.answer(
            "Chiqildi:",
            reply_markup=keyboardbutton(list(menus['user'][0].keys()), row=2)
        )
        await User_state.main_menu.set()
    elif text in categories():
        await state.update_data(changed_category=text)
        products_ = list(products(category=text))
        for i in menus["user"][0]['Mahsulotlar']: products_.append(i)
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await User_state.product.set()


async def user_product(m: m, state: s):
    data = await state.get_data()
    category_ = data.get('changed_category')
    text = m.text
    if text == "Chiqish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["user"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await User_state.categories.set()
    elif text in products(category_):
        await state.update_data(changed_product=text)
        product_data = product(category=category_, product=text)
        try:
            if product_data[3][-4:] == ".jpg":
                photo = InputFile(product_data[3])
            elif product_data[3][-4:] == ".mp4":
                video = InputFile(product_data[3])
            else:
                photo, video = False, False
        except Exception as _:
            photo, video = False, False
        caption = f"{product_data[0]}\n" \
                  f"{product_data[1]}\n" \
                  f"{product_data[2]}"
        if photo:
            await m.answer_photo(photo=photo, caption=caption, reply_markup=keyboardbutton(["Buyurtma berish",
                                                                                            "Chiqish"]))
        elif video:
            await m.answer_video(video=video, caption=caption, reply_markup=keyboardbutton(["Buyurtma berish",
                                                                                            "Chiqish"]))
        else:
            await m.answer(text=caption, reply_markup=keyboardbutton(["Buyurtma berish",
                                                                      "Chiqish"]))
        await User_state.product_buy.set()


async def product_buy(m: m, state: s):
    if m.text == "Chiqish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["user"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await User_state.categories.set()
    elif m.text == "Buyurtma berish":
        await m.answer("Mahsulot sonini kiriting:", reply_markup=keyboardbutton(["Chiqish"]))
        await User_state.product_count.set()


async def product_count(m: m, state: s):
    if m.text == "Chiqish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["user"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await User_state.categories.set()
    elif m.text.isdigit():
        if int(m.text) > 0:
            user = get_user_by_tg_id(tg_id=m.chat.id)
            await state.update_data(number_of_orders=m.text)
            await m.answer(
                f"F.I: {user['name']}\n"
                f"Telefon: {user['phone_number']}\n"
                f"Aloqa: {user['aloqa']}\n"
                f"Viloyat: {user['viloyat']}\n"
                f"Tuman: {user['tuman']}\n"
                f"Manzil: {user['address']}\n"
            )
            await m.answer(f"Malumotlaringizni tasdiqlaysizmi:",
                           reply_markup=keyboardbutton(["Tasdiqlash", "O'zgartirish",
                                                        "Bekor qilish"], row=2))
            await User_state.product_buy_menu.set()


async def product_buy_menu(m: m, state: s):
    if m.text == "Tasdiqlash":
        database = await state.get_data()
        prid = get_product_id(name=database.get("changed_product"), category=database.get("changed_category"))
        if prid:
            if add_order(product=prid, number_of_orders=database.get("number_of_orders"), user_tg_id=m.from_user.id):
                await m.answer("Mahsulot muvaffaqiyatli buyurtma qilindi.")
                categories_mal = categories()
                if categories_mal is None:
                    categories_mal = []

                for i in menus["user"][0]['Mahsulotlar']: categories_mal.append(i)
                await m.answer(
                    "Mahsulot turini tanlang:",
                    reply_markup=keyboardbutton(categories_mal)
                )
                await User_state.categories.set()
            else:
                await m.answer("Mahsulotni buyurtma qilishni iloji bo'lmadi.")
        else:
            await m.answer("Mahsulotni buyurtma qilishni iloji bo'lmadi.")
    elif m.text == "O'zgartirish":
        await m.answer("O'zgartirmoqchi bo'lgan malumotingizni tanlang:", reply_markup=keyboardbutton(["F.I",
                                                                                                       "Telefon",
                                                                                                       "Aloqa",
                                                                                                       "Viloyat",
                                                                                                       "Tuman",
                                                                                                       "Manzil",
                                                                                                       "Bekor "
                                                                                                       "qilish"],
                                                                                                      row=2))
        await User_state.change_about.set()
    elif m.text == "Bekor qilish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["user"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await User_state.categories.set()


async def user_change_about(m: m, state: s):
    if m.text in ("F.I", "Telefon", "Aloqa", 'Viloyat', "Tuman", "Manzil"):
        await m.answer("Yangi malumotni kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await state.update_data(change_about=m.text)
        await User_state.change_about_.set()

    elif m.text == "Bekor qilish":
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlarni o'zgartirish bekor qilindi. Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash",
                                                    "O'zgartirish",
                                                    "Bekor qilish"], row=2))
        await User_state.product_buy.set()


async def user_change_about_(m: m, state: s):
    if m.text == "Bekor qilish":
        user = get_user_by_tg_id(tg_id=m.chat.id)
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await m.answer(f"Malumotlarni o'zgartirish bekor qilindi. Malumotlaringizni tasdiqlaysizmi:",
                       reply_markup=keyboardbutton(["Tasdiqlash",
                                                    "O'zgartirish",
                                                    "Bekor qilish"], row=2))
        await User_state.product_buy.set()
    else:
        data = await state.get_data()
        change_about = data.get("change_about")
        uid = get_user_by_tg_id(tg_id=m.from_user.id)["id"]
        re = False
        if change_about == "F.I":
            if change_user_data(user_id=uid, name=m.text):
                re = True
        elif change_about == "Telefon":
            if change_user_data(user_id=uid, phone_number=m.text):
                re = True
        elif change_about == "Aloqa":
            if change_user_data(user_id=uid, aloqa=m.text):
                re = True
        elif change_about == "Viloyat":
            if change_user_data(user_id=uid, viloyat=m.text):
                re = True
        elif change_about == "Tuman":
            if change_user_data(user_id=uid, tuman=m.text):
                re = True
        elif change_about == "Manzil":
            if change_user_data(user_id=uid, address=m.text):
                re = True

        if re:
            user = get_user_by_tg_id(tg_id=m.chat.id)
            await m.answer(
                f"F.I: {user['name']}\n"
                f"Telefon: {user['phone_number']}\n"
                f"Aloqa: {user['aloqa']}\n"
                f"Viloyat: {user['viloyat']}\n"
                f"Tuman: {user['tuman']}\n"
                f"Manzil: {user['address']}\n"
            )
            await m.answer(f"Malumotlaringizni tasdiqlaysizmi:",
                           reply_markup=keyboardbutton(["Tasdiqlash", "O'zgartirish",
                                                        "Bekor qilish"], row=2))
            await User_state.product_buy_menu.set()