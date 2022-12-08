from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram import types as tp

titles = {
    'new_tips': 'Новый день, новый чай!',
    'update_data': 'Обновить данные',
    'decade_stat': 'Статстика за декаду'
}

tip_systems = {
    'KM': 'KateMedia',
    'nm': 'нет монет',
    'cash': 'Наличка'
}


def create_main_keyboard():
    kb = [
        [tp.KeyboardButton(text=titles['new_tips'])],
        [
            tp.KeyboardButton(text=titles['update_data']),
            tp.KeyboardButton(text=titles['decade_stat'])
         ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Чё делать будем?...'
    )


def create_tip_system():
    kb = [
        [
            tp.KeyboardButton(text=tip_systems['KM']),
            tp.KeyboardButton(text=tip_systems['nm']),
            tp.KeyboardButton(text=tip_systems['cash'])
        ],
        [tp.KeyboardButton(text='Готово')]
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Где чай считаем?...'
    )
