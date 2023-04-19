"""
states
"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class Supadmin_state(StatesGroup):
    """
    main state
    """
    main_menu = State()

class Admin_state(StatesGroup):
    """
    main state
    """
    main_menu = State()
    categories = State()
    changed_category = State()
    product = State()
    changed_product = State()
    add_category = State()
    add_product_name = State()
    add_product_about = State()
    add_product_price = State()
    add_product_photo = State()
    add_product = State()
    product_menu = State()


class User_state(StatesGroup):
    """
    main state
    """
    main_menu = State()
    categories = State()
    changed_category = State()
    product = State()
    product_menu = State()
    product_buy = State()
    change_about_ = State()
    change_about = State()
    product_count = State()
    product_buy_menu = State()
    change_data_personal = State()
    change_data_personal_ = State()
    change_data_personal_acces = State()