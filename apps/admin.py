"""
admin
"""
from aiogram.types import Message as m, InputFile
from aiogram.dispatcher import FSMContext as s

from buttons.inlinekeyboardbuttons import product_forward, inlinekeyboardbutton
from buttons.keyboardbuttons import keyboardbutton
from config import menus
from database.database import categories, products, product, remove_category, add_category, add_product_, \
    remove_product, orders_to_excel
from states import Admin_state


async def admin_main_menu(m: m, state: s):
    text = m.text
    if text == "Mahsulotlar":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["admin"][0]['Mahsulotlar']:categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await Admin_state.categories.set()
    elif m.text == "Buyurtmalar":
        filename = f"database/excels/orders.xlsx"
        orders_to_excel(filename)
        file = InputFile(filename)
        await m.answer_document(document=file, caption="Orders")


async def admin_categories_f(m:m, state: s):
    text = m.text
    if text == "Chiqish":
        await m.answer(
            "Chiqildi:",
            reply_markup=keyboardbutton(list(menus['admin'][0].keys()), row=2)
        )
        await Admin_state.main_menu.set()
    elif text in categories():
        await state.update_data(changed_category=text)
        products_ = list(products(category=text))
        for i in menus["admin"][0]['Mahsulotlar']:products_.append(i)
        products_.append("Turni o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    elif text == "Qo'shish":
        await state.update_data(changed_category=text)
        await m.answer("Yangi tur nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.add_category.set()


async def admin_category_add(m: m, state: s):
    data = await state.get_data()
    text = m.text
    if text == "Bekor qilish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["admin"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )

        await Admin_state.categories.set()
    else:
        if add_category(text):
            await m.answer(
                text="Tur muvaffaqiyatli qoshildi"
            )
        else:
            await m.answer(
                text="Tur muvaffaqiyatli qoshilmadi"
            )
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []
        for i in menus["admin"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await Admin_state.categories.set()


async def admin_product(m: m, state: s):
    data = await state.get_data()
    category_ = data.get('changed_category')
    text = m.text
    if text == "Chiqish":
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["admin"][0]['Mahsulotlar']:categories_mal.append(i)
        await m.answer(
            "Mahsulot turini tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await Admin_state.categories.set()
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
            await m.answer_photo(photo=photo, caption=caption, reply_markup=keyboardbutton(["O'chirish", "Chiqish"]))
        elif video:
            await m.answer_video(video=photo, caption=caption, reply_markup=keyboardbutton(["O'chirish", "Chiqish"]))
        else:
            await m.answer(text=caption, reply_markup=keyboardbutton(["O'chirish", "Chiqish"]))
        await Admin_state.product_menu.set()
    elif text == "Qo'shish":
        await state.update_data(changed_product=text)
        await m.answer("Yangi mahsulotning nomini kiriting:", reply_markup=keyboardbutton(["Bekor qilish"]))
        await Admin_state.add_product_name.set()
    elif text == "Turni o'chirish":
        if remove_category(category_):
            await m.answer("Tur muvafaqiyatli o'chirildi!")
        else:
            await m.answer("Categoriyani o'chirishni iloji bo'lmadi!")
        categories_mal = categories()
        if categories_mal is None:
            categories_mal = []

        for i in menus["admin"][0]['Mahsulotlar']: categories_mal.append(i)
        await m.answer(
            "categoriyani tanlang:",
            reply_markup=keyboardbutton(categories_mal)
        )
        await Admin_state.categories.set()


async def admin_product_menu(m: m, state: s):
    textwrap = m.text
    if textwrap == "Chiqish":
        data = await state.get_data()
        products_ = list(products(category=data.get("changed_category")))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    elif textwrap == "O'chirish":
        data = await state.get_data()
        if remove_product(product_name=data.get('changed_product'), category_name=data.get("changed_category")):
            await m.answer(
                text="Mahsulot muvaffaqiyatli o'chirildi."
            )
        else:
            await m.answer(
                text="Mahsulot muvafaqiyatli o'chirilmadi."
            )
        data = await state.get_data()
        products_ = list(products(category=data.get("changed_category")))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()


async def add_product_name(m: m, state: s):
    text = m.text
    if text == "Bekor qilish":
        data = await state.get_data()
        category = data.get("changed_category")
        products_ = list(products(category=category))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    else:
        if 7 < len(str(text)) < 100:
            await state.update_data(add_product_name=text)
            await m.answer(
                text="Mahsulot haqida batafsil malumot kiriting:",
                reply_markup=keyboardbutton(["Bekor qilish"])
            )
            await Admin_state.add_product_about.set()
        else:
            await m.answer("Mahsulot nomi 100 simvoldan oshmasligi 7 simvoldan kam bo'lmasligi kerak kerak va matn, "
                           "raqamlardan "
                           "tashkil topishi mumkin.")


async def add_product_about(m: m, state: s):
    text = m.text
    if text == "Bekor qilish":
        data = await state.get_data()
        category = data.get("changed_category")
        products_ = list(products(category=category))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    else:
        if 7 < len(str(text)) < 500:
            await m.answer(
                text="Mahsulot haqida vide yoki rasm jo'nating:",
                reply_markup=keyboardbutton(["Bekor qilish"])
            )
            await state.update_data(add_product_about=m.text)
            await Admin_state.add_product_photo.set()
        else:
            await m.answer("Mahsulot malumoti 500 simvoldan oshmasligi, 7 simvoldan kam bo'lmasligi kerak va "
                           "matn, raqamlardan "
                           "tashkil topishi "
                           "mumkin.")


async def add_product_photo(m: m, state: s):
    if m.photo:
        photo = m.photo[-1]
        photo_name = f"database/media/photo_{m.from_user.id}_{m.message_id}.jpg"
        await state.update_data(add_product_photo=photo_name)
        await photo.download(photo_name)
        await m.reply("Rahmat! Rasm qabul qilindi.")
        await m.answer("Mahsulot narhini kiriting:")
        await Admin_state.add_product_price.set()
    elif m.video:
        video = m.video
        video_name = f"database/media/video_{m.from_user.id}_{video.file_id}.mp4"
        await state.update_data(add_product_photo=video_name)
        await video.download(video_name)
        await m.reply("Rahmat! Video qabul qilindi.")
        await m.answer("Mahsulot narhini kiriting:")
        await Admin_state.add_product_price.set()
    elif m.text:
        text = m.text
        if text == "Bekor qilish":
            data = await state.get_data()
            category = data.get("changed_category")
            products_ = list(products(category=category))
            for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
            products_.append("Categoriyani o'chirish")
            btn = keyboardbutton(products_)
            await m.answer(
                text="Mahsulotni tanlang:",
                reply_markup=btn
            )
            await Admin_state.product.set()


async def add_product_price(m: m, state: s):
    text = m.text
    if text == "Bekor qilish":
        data = await state.get_data()
        category = data.get("changed_category")
        products_ = list(products(category=category))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    else:
        data = await state.get_data()
        add_product_name = data.get("add_product_name")
        add_product_about = data.get("add_product_about")
        add_product_media = data.get("add_product_photo")
        add_product_price = m.text
        if add_product_media[-4:] == ".jpg":
            await m.answer_photo(
                photo=InputFile(add_product_media),
                caption=f"name: {add_product_name}\n"
                      f"about: {add_product_about}\n"
                      f"price: {add_product_price}"
            )
        elif add_product_media[-4:] == ".mp4":
            await m.answer_video(
                video=InputFile(add_product_media),
                caption=f"name: {add_product_name}\n"
                      f"about: {add_product_about}\n"
                      f"price: {add_product_price}"
            )
        await state.update_data(add_product_price=add_product_price)
        await m.answer("Mahsulotning ko'rinishini tasdiqlaysizmi?", reply_markup=keyboardbutton(["Tasdiqlash",
                                                                                                 "Bekor qilish"]))
        await Admin_state.add_product.set()


async def add_product(m: m, state: s):
    text = m.text
    if text == "Bekor qilish":
        data = await state.get_data()
        category = data.get("changed_category")
        products_ = list(products(category=category))
        for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
        products_.append("Categoriyani o'chirish")
        btn = keyboardbutton(products_)
        await m.answer(
            text="Mahsulotni tanlang:",
            reply_markup=btn
        )
        await Admin_state.product.set()
    elif text == "Tasdiqlash":
        data = await state.get_data()
        category = data.get("changed_category")
        add_product_name = data.get("add_product_name")
        add_product_about = data.get("add_product_about")
        add_product_price = data.get("add_product_price")
        add_product_media = data.get("add_product_photo")
        if add_product_(
            name=add_product_name,
            category=category,
            about=add_product_about,
            price=add_product_price,
            photo=add_product_media
        ):
            products_ = list(products(category=category))
            for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
            products_.append("Categoriyani o'chirish")
            btn = keyboardbutton(products_)
            await m.answer("Mahsulot qo'shish muvaffaqiyatli yakunlandi.")
            await m.answer(
                text="Mahsulotni tanlang:",
                reply_markup=btn
            )
            await Admin_state.product.set()
        else:
            await m.answer("Mahsulot qo'shish muvaffaqiyatsiz yakunlandi.")
            data = await state.get_data()
            category = data.get("changed_category")
            products_ = list(products(category=category))
            for i in menus["admin"][0]['Mahsulotlar']: products_.append(i)
            products_.append("Categoriyani o'chirish")
            btn = keyboardbutton(products_)
            await m.answer(
                text="Mahsulotni tanlang:",
                reply_markup=btn
            )
            await Admin_state.product.set()
