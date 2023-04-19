"""
buttons inline
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def inlinekeyboardbutton(product_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text='Buyurtma berish', callback_data=f"shop_product_id_{product_id}"),
    )
    return keyboard


def product_forward(url):
    forward_callback = CallbackData('forward', 'message_id')
    forward_button = InlineKeyboardButton('Forward', url=url)
    forward_keyboard = InlineKeyboardMarkup().add(forward_button)
    return forward_keyboard
