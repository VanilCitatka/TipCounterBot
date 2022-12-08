from aiogram import Router, types as tp
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext

from db.crud import get_decade_statistic
from db.database import SessionLocal
from gags.keyboards import titles, create_main_keyboard, create_tip_system
from gags.new_tip_manager import TipFSM, t_manager

router = Router(name='Квинтэссенция')
router.include_router(t_manager)


@router.message(Command(commands=['start']))
async def bot_init(message: tp.Message):
    await message.answer(
        'Привет! Я посчитаю твои чаявые за день! :)',
        reply_markup=create_main_keyboard()
    )


@router.message(Text(text=titles['new_tips']))
async def new_tips(message: tp.Message, state: FSMContext):
    await state.set_state(TipFSM.tips_manager)
    await message.answer('Чё по чаю за сегодня?', reply_markup=create_tip_system())
    await state.update_data(km_tips='0')
    await state.update_data(nm_tips='0')
    await state.update_data(cash_tips='0')


@router.message(Text(text=titles['decade_stat']))
async def decade_stat(msg: tp.Message):
    with SessionLocal() as session:
        stats = get_decade_statistic(session)
        print(stats)
    for row in stats:
        await msg.answer(f'Дата: {row.date} - Сумма чая: {row.tip_sum}')
