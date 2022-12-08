from typing import Dict, Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, types as tp, F
from aiogram.filters import Text
from db.models import Base
from db.database import SessionLocal, engine
from db.crud import create_tip_day

from .keyboards import tip_systems, create_main_keyboard, create_tip_system

t_manager = Router(name='Пенис')


class TipFSM(StatesGroup):
    tips_manager = State()
    money_wait = State()


@t_manager.message(
    TipFSM.tips_manager,
    Text(text=[tip_systems['KM']])
)
async def km_tips_handler(message: tp.Message, state: FSMContext):
    await message.answer('Ну и сколько чая в KateMedia?', reply_markup=None)
    await state.update_data(wait_from='km')
    await state.set_state(TipFSM.money_wait)


@t_manager.message(
    TipFSM.tips_manager,
    Text(text=[tip_systems['nm']])
)
async def nm_tips_handler(message: tp.Message, state: FSMContext):
    await message.answer('Ну и сколько чая в нет монет?', reply_markup=None)
    await state.update_data(wait_from='nm')
    await state.set_state(TipFSM.money_wait)


@t_manager.message(
    TipFSM.tips_manager,
    Text(text=[tip_systems['cash']])
)
async def cash_tips_handler(message: tp.Message, state: FSMContext):
    await message.answer('Ну и сколько чая наличкой??', reply_markup=None)
    await state.update_data(wait_from='cash')
    await state.set_state(TipFSM.money_wait)


@t_manager.message(
    TipFSM.money_wait,
    F.text.regexp(r'\d+')
)
async def set_money(message: tp.Message, state: FSMContext):
    data = await state.get_data()
    match data['wait_from']:
        case 'km':
            await state.update_data(km_tips=message.text)
            await message.answer(f'В KateMedia дали {message.text} рублей')
        case 'nm':
            await state.update_data(nm_tips=message.text)
            await message.answer(f'В нет монет дали {message.text} рублей')
        case 'cash':
            await state.update_data(cash_tips=message.text)
            await message.answer(f'Наличкой дали {message.text} рублей')
    await state.set_state(TipFSM.tips_manager)
    await message.answer('Ещё чё нить?', reply_markup=create_tip_system())


@t_manager.message(
    TipFSM.money_wait
)
async def wrong_message(msg: tp.Message):
    await msg.answer('Пиши цифрами!')


async def count_tips(message: tp.Message, data: Dict[str, Any]):
    km, nm, cash = data['km_tips'], data['nm_tips'], data['cash_tips']
    tip_sum = str(sum(map(int, (km, nm, cash))))
    await message.answer(f'KateMedia: {km} р.\nнет монет: {nm} р.\nНаличка: {cash}\nИтого: {tip_sum} р.')


@t_manager.message(
    TipFSM.tips_manager,
    Text(text='Готово')
)
async def done(msg: tp.Message, state: FSMContext):
    data = await state.get_data()
    await msg.answer("Всё, почитали:", reply_markup=create_main_keyboard())
    await count_tips(message=msg, data=data)
    with SessionLocal() as session:
        create_tip_day(session, data=data)
    await state.clear()
