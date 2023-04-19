"""
app file
"""
from aiogram.types import ContentType as ct

from apps.admin import *
from apps.user import user_main_menu, user_product, user_categories_f, product_buy_menu, \
    product_count, user_change_about, user_change_about_, product_buy, change_data_personal, \
    change_data_personal_address, change_data_personal_fi, change_data_personal_telefon, change_data_personal_aloqa, \
    change_data_personal_viloyat, change_data_personal_tuman, change_data_personal_buy
from loader import dp
# from states import *
from apps.login import \
    cmd_start
from states import User_state, Admin_state

# cmd start
dp.register_message_handler(cmd_start, content_types=[ct.TEXT])

"""
ADMIN APPS
"""

# main_menu

dp.register_message_handler(admin_main_menu, content_types=[ct.TEXT], state=Admin_state.main_menu)

# category

dp.register_message_handler(admin_categories_f, content_types=[ct.TEXT], state=Admin_state.categories)
dp.register_message_handler(admin_category_add, content_types=[ct.TEXT], state=Admin_state.add_category)

# product

dp.register_message_handler(admin_product, content_types=[ct.TEXT], state=Admin_state.product)
## add product
dp.register_message_handler(add_product_name, content_types=[ct.TEXT], state=Admin_state.add_product_name)
dp.register_message_handler(add_product_about, content_types=[ct.TEXT], state=Admin_state.add_product_about)
dp.register_message_handler(add_product_photo, content_types=[ct.TEXT, ct.VIDEO, ct.PHOTO],
                            state=Admin_state.add_product_photo)
dp.register_message_handler(add_product_price, content_types=[ct.TEXT], state=Admin_state.add_product_price)
dp.register_message_handler(add_product, content_types=[ct.TEXT], state=Admin_state.add_product)
## remove product
dp.register_message_handler(admin_product_menu, content_types=[ct.TEXT], state=Admin_state.product_menu)

"""
USER APPS
"""

# main_menu

dp.register_message_handler(user_main_menu, content_types=[ct.TEXT], state=User_state.main_menu)

# category

dp.register_message_handler(user_categories_f, content_types=[ct.TEXT], state=User_state.categories)

# product

dp.register_message_handler(user_product, content_types=[ct.TEXT], state=User_state.product)
dp.register_message_handler(product_buy, content_types=[ct.TEXT], state=User_state.product_buy)
dp.register_message_handler(product_count, content_types=[ct.TEXT], state=User_state.product_count)
dp.register_message_handler(product_buy_menu, content_types=[ct.TEXT], state=User_state.product_buy_menu)
dp.register_message_handler(user_change_about, content_types=[ct.TEXT], state=User_state.change_about)
dp.register_message_handler(user_change_about_, content_types=[ct.TEXT], state=User_state.change_about_)

# data
dp.register_message_handler(change_data_personal, content_types=[ct.TEXT], state=User_state.change_data_personal)
dp.register_message_handler(change_data_personal_address, content_types=[ct.TEXT],
                            state=User_state.change_data_personal_address)

# add data
dp.register_message_handler(change_data_personal_buy, content_types=[ct.TEXT], state=User_state.change_data_personal_buy)
dp.register_message_handler(change_data_personal_fi, content_types=[ct.TEXT], state=User_state.change_data_personal_fi)
dp.register_message_handler(change_data_personal_telefon, content_types=[ct.TEXT], state=User_state.change_data_personal_telefon)
dp.register_message_handler(change_data_personal_aloqa, content_types=[ct.TEXT], state=User_state.change_data_personal_aloqa)
dp.register_message_handler(change_data_personal_viloyat, content_types=[ct.TEXT], state=User_state.change_data_personal_viloyat)
dp.register_message_handler(change_data_personal_tuman, content_types=[ct.TEXT], state=User_state.change_data_personal_tuman)
