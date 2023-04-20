"""
user
"""
from aiogram.types import Message as m, InputFile, CallbackQuery, InlineQuery, callback_query
from aiogram.dispatcher import FSMContext as s, FSMContext

from buttons.inlinekeyboardbuttons import inlinekeyboardbutton
from buttons.keyboardbuttons import keyboardbutton
from config import menus
from database.database import categories, products, product, get_user_by_tg_ids as get_user_by_tg_id, add_order, \
    get_product_id, \
    change_user_data, get_orders_by_user_tg_id, get_product_all_data_by_id, add_new_user, get_user_by_id_ids
from loader import bot
from states import User_state


async def user_main_menu(m: m, state: s):
    if m.text == "Mahsulotlar":
        await state.update_data(buying="False")
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
        await state.update_data(buying="False")
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
            user = get_user_by_id_ids(data[6])
            caption = f"{product_data[0]}\n" \
                      f"{product_data[1]}\n" \
                      f"{product_data[2]}\n" \
                      f"Buyurtma soni: {data[2]}\n" \
                      f"Kament: {data[3]}\n" \
                      f"F.I: {user['name']}\n" \
                      f"Telefon: {user['phone_number']}\n" \
                      f"Aloqa: {user['aloqa']}\n" \
                      f"Viloyat: {user['viloyat']}\n" \
                      f"Tuman: {user['tuman']}\n" \
                      f"Manzil: {user['address']}\n"
            if photo:
                await m.answer_photo(photo=photo, caption=caption)
            elif video:
                await m.answer_video(video=video, caption=caption)
            else:
                await m.answer(text=caption)
    elif m.text == "Mening ma'lumotlarim":
        await state.update_data(buying="False")
        user = get_user_by_tg_id(tg_id=m.chat.id)
        btns = ["Chiqish", "O'zgartirish"]
        await m.answer(f"Malumotlaringiz:",
                       reply_markup=keyboardbutton(btns, row=2))
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )
        await User_state.change_data_personal.set()

async def change_data_personal(m: m, state: s):
    if m.text == "O'zgartirish":
        await m.answer("F.I:", reply_markup=keyboardbutton(["Bekor qilish"],row=2))
        await User_state.change_data_personal_fi.set()
    elif m.text == "Chiqish" or m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()


async def change_data_personal_fi(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()

    else:
        await state.update_data(change_data_personal_fi=m.text)
        await m.answer("Telefon raqam kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await User_state.change_data_personal_telefon.set()


async def change_data_personal_telefon(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()

    else:
        await state.update_data(change_data_personal_telefon=m.text)
        await m.answer("Bog'lanish uchun qo'shimcha malumot kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await User_state.change_data_personal_aloqa.set()


async def change_data_personal_aloqa(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()

    else:
        await state.update_data(change_data_personal_aloqa=m.text)
        await m.answer("Viloyatingizni tanlang:", reply_markup=keyboardbutton(["Toshkent vil","Toshkent sh",
                                                                               "Namangan","Andijon","Farg'ona",
                                                                               "Navoiy","Xorazm","Buxoro","Jizzax",
                                                                               "Qashqadaryo","Qoraqalpog'iston res",
                                                                               "Samarqand","Sirdaryo","Surxondaryo",
                                                                               "Bekor qilish"], row=2))
        await User_state.change_data_personal_viloyat.set()

async def change_data_personal_viloyat(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()

    else:
        await state.update_data(change_data_personal_viloyat=m.text)
        await m.answer("Tumaningizni kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await User_state.change_data_personal_tuman.set()

async def change_data_personal_tuman(m: m, state: s):
    if m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()

    else:
        await state.update_data(change_data_personal_tuman=m.text)
        await m.answer("Manzilingiz haqida qo'shimcha malumot kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await User_state.change_data_personal_address.set()


async def change_data_personal_address(m: m, state: s):
    if m.text == "Bekor qilish":
        database = await state.get_data()
        if bool(database.get("buying")):
            user = get_user_by_tg_id(tg_id=m.chat.id)
            await state.update_data(number_of_orders=m.text)
            user = get_user_by_tg_id(tg_id=m.chat.id)
            btns = []
            for i in list(user.keys()): btns.append(i)
            btns += ["Chiqish", "Qo'shish"]
            await m.answer(f"Malumotlaringiz:",
                           reply_markup=keyboardbutton(btns, row=2))
            await state.update_data(buying="True")
            await User_state.change_data_personal_buy.set()
        else:
            await m.answer(
                "Asosiy menyu:",
                reply_markup=keyboardbutton(
                    btns=list(menus[
                                  'user'][0].keys())))
            await User_state.main_menu.set()
    else:
        user = await state.get_data()

        # await m.answer(
        #     f"F.I: {user['change_data_personal_fi']}\n"
        #     f"Telefon: {user['change_data_personal_telefon']}\n"
        #     f"Aloqa: {user['change_data_personal_aloqa']}\n"
        #     f"Viloyat: {user['change_data_personal_viloyat']}\n"
        #     f"Tuman: {user['change_data_personal_tuman']}\n"
        #     f"Manzil: {m.text}\n"
        # )
        if add_new_user(
            user['change_data_personal_fi'],
            user['change_data_personal_telefon'],
            user['change_data_personal_aloqa'],
            user['change_data_personal_viloyat'],
            user['change_data_personal_tuman'],
            m.text,
            m.chat.id,
        ):
            await m.answer(f"Malumotlaringizni muvaffaqiyatli saqlandi.")
        else:
            await m.answer(f"Malumotlaringizni muvaffaqiyatli saqlanmadi.")
        user = get_user_by_tg_id(tg_id=m.chat.id)
        btns = []
        for i in list(user.keys()): btns.append(i)
        btns += ["Chiqish", "Qo'shish"]
        await m.answer(f"Malumotlaringiz:",
                       reply_markup=keyboardbutton(btns, row=2))
        database = await state.get_data()
        buying = database.get("buying")
        await state.update_data(buying="False")
        await m.answer(
            f"F.I: {user['name']}\n"
            f"Telefon: {user['phone_number']}\n"
            f"Aloqa: {user['aloqa']}\n"
            f"Viloyat: {user['viloyat']}\n"
            f"Tuman: {user['tuman']}\n"
            f"Manzil: {user['address']}\n"
        )

        if buying == "True":
            await User_state.change_data_personal_buy.set()
        else:
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
        database = await state.get_data()
        category_ = database.get("changed_category")
        product_ = database.get("changed_product")
        product_data = product(category=category_, product=product_)

        await m.answer(f"Mahsulot sonini tanlang:\n"
                       f"1 ta mahsulot {product_data[2]}\n"
                       f"3 (1+1=3) ta mahsulot {float(product_data[2])*2}", reply_markup=keyboardbutton(["1","3",
                                                                                                       "Chiqish"]))
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
            await state.update_data(number_of_orders=m.text)
            user = get_user_by_tg_id(tg_id=m.chat.id)
            btns = ["Tasdiqlash", "O'zgartirish", "Chiqish"]
            await m.answer(f"Malumotlaringiz:",
                           reply_markup=keyboardbutton(btns, row=2))
            await m.answer(
                f"F.I: {user['name']}\n"
                f"Telefon: {user['phone_number']}\n"
                f"Aloqa: {user['aloqa']}\n"
                f"Viloyat: {user['viloyat']}\n"
                f"Tuman: {user['tuman']}\n"
                f"Manzil: {user['address']}\n"
            )
            await state.update_data(buying="True")
            await User_state.change_data_personal_buy.set()


async def change_data_personal_buy(m: m, state: s):
    if m.text == "O'zgartirish:":
        await m.answer("F.I:", reply_markup=keyboardbutton(["Bekor qilish"], row=2))
        await User_state.change_data_personal_fi.set()
    elif m.text == "Chiqish" or m.text == "Bekor qilish":
        await m.answer(
            "Asosiy menyu:",
            reply_markup=keyboardbutton(
                btns=list(menus[
                              'user'][0].keys())))
        await User_state.main_menu.set()
    elif m.text == "Tasdiqlash":
        await m.answer("Cament kiriting:", reply_markup=keyboardbutton(["Tashlab ketish", "Bekor qilish"]))
        await User_state.product_buy_menu.set()
async def product_buy_menu(m: m, state: s):
    if m.text == "Bekor qilish":
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
        if m.text == "Tashlab ketish":cament="Kiritilmagan"
        else:cament = m.text
        database = await state.get_data()
        prid = get_product_id(name=database.get("changed_product"), category=database.get("changed_category"))
        if prid:
            user = get_user_by_tg_id(tg_id=m.chat.id)
            if add_order(product=prid, number_of_orders=database.get("number_of_orders"),cament=cament ,
                         user_tg_id=m.from_user.id, user_id=user["id"]):
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