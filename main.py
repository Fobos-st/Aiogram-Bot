from config import TOKEN_API
from Button import *
from text import *
from aiogram import *
from aiogram import Bot, Dispatcher, types
from sqlite import *
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton('/help'))
    await message.answer('<b>Добро пожаловать!</b>',
                         parse_mode='html',
                         reply_markup=kb,
                         )
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           text=HELP_COMMAND,
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['idea'])
async def idea_command(message: types.Message):
    await bot.send_message(message.chat.id,
                           text=IDEA,
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands=['IdeaForBot'])
async def idea_command(message: types.Message):
    await bot.send_message(1254191582, f"Идея от пользователя @{message.from_user.first_name} \n {message.text[12:]}")
    await bot.send_message(message.chat.id, f'Ваша идея: "{message.text[12:]}" \nИдея была отправлена')
    await message.answer(f"Ваш ID: {message.from_user.id}")


@dp.message_handler(commands=['CuteCat'])
async def send_sticker_and_text(message: types.Message):
    await message.reply('Смотри какой милый котик 😺')
    sticker = 'CAACAgIAAxkBAAEHx9Nj73gW0_j9iGR08e_L8S5KGpxztAACXxMAAi5eyEvZq78wYISWMy4E'
    await bot.send_sticker(message.chat.id, sticker=sticker)
    await message.delete()


@dp.message_handler(commands='MemberChat')
async def chat_member_cmd(message: types.Message):
    await bot.send_message(message.chat.id, f'Количество участников '
                                            f'{await bot.get_chat_members_count(chat_id=message.chat.id)}')


@dp.message_handler(commands=['UserID'])
async def cmd_id_user(message: types.Message):
    await bot.send_message(message.chat.id, f'User id:{message.reply_to_message.from_user.id}')


@dp.message_handler(commands='AdminList')
async def cmd_admin_list(message: types.Message):
    admin_list = 'Список админов:\n'
    chat_admins = await bot.get_chat_administrators(message.chat.id)
    for admins in chat_admins:
        user_id = admins.user.first_name
        if user_id == 'Fobos Чат-менеджер':
            continue
        else:
            admin_list += "@{}\n".format(user_id)
    await message.answer(admin_list)


@dp.message_handler(commands='ban')
async def cmd_admin_list(message: types.Message):
    user_id = message.reply_to_message.from_user.id
    chat_id = message.chat.id
    chat_admins = await bot.get_chat_administrators(message.chat.id)
    for admins in chat_admins:
        user_i = admins.user.id
        if user_i == message.from_user.id:
            await bot.ban_chat_member(chat_id, user_id=user_id, until_date=41)
            await message.answer(f'Пользователь {message.reply_to_message.from_user.first_name}\n Заблокирован')
            return
    await message.answer('У вас недостаточно прав')


# Правильный сон


@dp.message_handler(commands=['GoodSleep'])
async def start_course(message: types.Message):
    sc = f"""
    Привет {message.from_user.first_name}, ты начал проходить курс🥳
В этом курсе ты узнаешь основы, так сказать базу, о правильном сне
    """
    stic = 'CAACAgIAAxkBAAEIEilkCrK1FQFr9p5PASRF2-Kkn7iCvgACZQADJeuTHwtTiOp3nwAB0y8E'
    await bot.send_message(message.chat.id,
                           sc)
    await bot.send_sticker(message.chat.id,
                           sticker=stic)
    reg(message.from_user.id)
    kbmenu = ReplyKeyboardMarkup(row_width=1)
    if int(enter_source(message.from_user.id)) == 4:
        kbmenu.add(s_introduction, s_function, s_hygiene, s_basics)
    elif int(enter_source(message.from_user.id)) == 3:
        kbmenu.add(s_introduction, s_function, s_hygiene)
    elif int(enter_source(message.from_user.id)) == 2:
        kbmenu.add(s_introduction, s_function)
    elif int(enter_source(message.from_user.id)) == 1:
        kbmenu.add(s_introduction)
    await bot.send_message(chat_id=message.chat.id,
                           text=intro,
                           reply_markup=kbmenu)


@dp.message_handler(commands=['Вступление'])
async def intro_course(message: types.Message):
    await bot.send_message(message.chat.id,
                           '[Вступление](https://telegra.ph/Vstuplenie-03-11-3)',
                           parse_mode='MARKDOWN',
                           reply_markup=ReplyKeyboardRemove())
    new_source(message.from_user.id, 2)


@dp.message_handler(commands=['ФункцииСна'])
async def function_course(message: types.Message):
    await bot.send_message(message.chat.id,
                           '[Функции сна](https://telegra.ph/Funkcii-sna-03-13)',
                           parse_mode='MARKDOWN',
                           reply_markup=ReplyKeyboardRemove())
    new_source(message.from_user.id, 3)


@dp.message_handler(commands=['ГигиенаСна'])
async def function_course(message: types.Message):
    await bot.send_message(message.chat.id,
                           '[Гигиена сна](https://telegra.ph/Gigiena-Sna-03-15)',
                           parse_mode='MARKDOWN',
                           reply_markup=ReplyKeyboardRemove())
    new_source(message.from_user.id, 4)


@dp.message_handler(commands=['ОсновыСна'])
async def function_course(message: types.Message):
    await bot.send_message(message.chat.id,
                           '[Основы сна](https://telegra.ph/Osnovy-sna-03-16)',
                           parse_mode='MARKDOWN',
                           reply_markup=ReplyKeyboardRemove())


# Команады без '/'


@dp.message_handler()
async def cmd_in_chat(message: types.Message):
    if message.text[:8] == 'Обнять @':
        hugging = message.from_user.first_name
        embraced = message.text[6:]
        sticker = 'CAACAgIAAxkBAAEH3spj940gL3rABvpOiw-QGqHTBqEEWwACPQADwNw1NcAw3oYCt0JFLgQ'
        await bot.send_sticker(message.chat.id, sticker=sticker)
        await message.answer(f'@{hugging} обнял {embraced}')
        await message.delete()
    if message.text[:9] == 'Ударить @':
        beating = message.from_user.first_name
        victim = message.text[7:]
        await message.answer(f'@{beating} зачем-то ударил {victim}')
        await message.delete()
    if 'Казино' == message.text[:6]:
        balance = 0
        reg(message.from_user.id)
        for i in sql.execute(f"SELECT cash FROM users WHERE login = '{message.from_user.id}'"):
            balance = i[0]
        if 0 < int(message.text[6:]) <= balance:
            numbers = randint(1, 2)
            if numbers == 1:
                win_in_casino(message.from_user.id, message.text[6:])
                await bot.send_message(message.chat.id, 'You win')
                await message.answer(f'Ваш счёт: {enter(message.from_user.id)}')
            else:
                lose_in_casino(message.from_user.id, message.text[6:])
                await message.answer('You lose')
                await message.answer(f'Ваш счёт: {enter(message.from_user.id)}')
        else:
            if 0 >= int(message.text[6:]):
                await message.answer('Введите целое число')
            else:
                await message.answer('У вас недостаточно средств на счёте')
        if enter(message.from_user.id) == 0:
            gift = randint(500, 10000)
            await message.answer('Бот сегодня в хорошом настроение так что держи чутка')
            await message.answer(f'Вам перевели {gift}')
            gift_of_casino(message.from_user.id, gift)
            await message.answer(f'Ваш счёт: {enter(message.from_user.id)}')


if __name__ == '__main__':
    executor.start_polling(dp, allowed_updates=["message", "inline_query", "chat_member"],
                           skip_updates=True)
