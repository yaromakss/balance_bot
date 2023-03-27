from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def home_btn():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="Profile")
    )
    home_buttons.add(
        types.KeyboardButton(text="Time")
    )
    home_buttons.add(
        types.KeyboardButton(text="Gallery")
    )
    home_buttons.adjust(1, 2)
    return home_buttons


def gallery_btn():
    gallery_buttons = ReplyKeyboardBuilder()
    gallery_buttons.add(
        types.KeyboardButton(text="New photo")
    )
    gallery_buttons.add(
        types.KeyboardButton(text="Menu")
    )
    gallery_buttons.adjust(2)
    return gallery_buttons


def profile_btn():
    profile_buttons = ReplyKeyboardBuilder()
    profile_buttons.add(
        types.KeyboardButton(text="Check balance")
    )
    profile_buttons.add(
        types.KeyboardButton(text="Menu")
    )
    profile_buttons.adjust(2)
    return profile_buttons

