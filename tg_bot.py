import logging
from pathlib import Path

import telebot
from telebot.util import extract_arguments, extract_command, is_command

import config
import calculator
import tick_tack_toe
import deep_fashion2

Path('photos').mkdir(exist_ok=True)

API_TOKEN = config.token
NEW_GAME = None
ARROW_SYMBOL = '\u2198\uFE0F'

bot = telebot.TeleBot(API_TOKEN)

telebot.logging.basicConfig(filename='log.csv', level=logging.INFO, encoding='utf-8',
                            format=' %(asctime)s; %(levelname)s; %(message)s')

logger = telebot.logger
logger.setLevel(logging.INFO)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand('start', 'начало работы'),
        telebot.types.BotCommand('calc', 'использовать калькулятор'),
        telebot.types.BotCommand('game', 'играть в крестики-нолики'),
        telebot.types.BotCommand('photo', 'отправить фото для детекции одежды')
    ],
)

df2 = deep_fashion2.DeepFashion()


def log_message(msg, txt):
    logger.info(f'{msg.chat.id}; {msg.from_user.username}; '
                f'{msg.from_user.full_name}; {txt}')


@bot.message_handler(commands=['start'])
def start_message(message):
    log_message(message, message.text)
    bot.send_message(message.chat.id, 'Готов к работе!')


@bot.message_handler(commands=['calc'])
def calc_message(message):
    if extract_arguments(message.text):
        process_expression(message)
    else:
        log_message(message, message.text)
        msg = bot.reply_to(message, f'Введите выражение для вычисления {ARROW_SYMBOL}')
        bot.register_next_step_handler(msg, process_expression)


def process_expression(message):
    log_message(message, message.text)
    expr = extract_arguments(message.text) if is_command(message.text) else message.text
    text_result = str(calculator.get_result(expr.lower())).replace('.', ',').removesuffix(',0')
    reply = f'{expr} = {text_result}'
    log_message(message, reply)
    bot.send_message(message.chat.id, reply)


def show_game_field(lst):
    return '\n'.join([''.join(row) for row in lst])


@bot.message_handler(commands=['game'])
def game_message(message):
    log_message(message, message.text)
    global NEW_GAME
    if not NEW_GAME:
        NEW_GAME = tick_tack_toe.Game()
    process_game(message)


def process_game(message):
    if NEW_GAME.winner:
        reply = f'{show_game_field(NEW_GAME.buttons)}\n' \
                f'{NEW_GAME.winner_text}'
        NEW_GAME.restart_game()
        log_message(message, '\n' + reply)
        bot.send_message(message.chat.id, reply)
    else:
        reply = f'{show_game_field(NEW_GAME.buttons)}\n' \
                f'Введите номер ряда (от 1 до 3) и столбца (от 1 до 3) через дефис, например: "1-2" {ARROW_SYMBOL}'
        log_message(message, '\n' + reply)
        msg = bot.send_message(message.chat.id, reply)
        bot.register_next_step_handler(msg, process_next_move)


def process_next_move(message):
    log_message(message, message.text)
    if is_command(message.text):
        for handler in bot.message_handlers:
            if extract_command(message.text) in handler['filters']['commands']:
                handler['function'](message)
                return

    move = message.text.split('-')

    if len(move) != 2:
        reply = 'Неверный формат ввода, введите 2 числа через дефис.'
        log_message(message, reply)
        msg = bot.reply_to(message, reply)
        bot.register_next_step_handler(msg, process_next_move)
        return

    try:
        i, j = map(int, move)
    except ValueError:
        reply = 'Неверный формат ввода, вводите только целые числа.'
        log_message(message, reply)
        msg = bot.reply_to(message, reply)
        bot.register_next_step_handler(msg, process_next_move)
        return

    if i not in range(1, 4) or j not in range(1, 4):
        reply = 'Значения за пределами поля, вводите только числа от 1 до 3.'
        log_message(message, reply)
        msg = bot.reply_to(message, reply)
        bot.register_next_step_handler(msg, process_next_move)
        return

    i -= 1
    j -= 1
    if (i, j) not in NEW_GAME.available_buttons:
        reply = 'Поле уже занято, попробуйте ещё раз.'
        log_message(message, reply)
        msg = bot.reply_to(message, reply)
        bot.register_next_step_handler(msg, process_next_move)
        return

    NEW_GAME.toggle_field(i, j)
    process_game(message)


@bot.message_handler(commands=['photo'])
def photo_message(message):
    log_message(message, message.text)
    bot.send_message(message.chat.id, f'Пришлите фото для детекции предметов одежды {ARROW_SYMBOL}')


@bot.message_handler(content_types=['photo'])
def photo_reply(message):
    file_id = message.photo[-1].file_id
    log_message(message, file_id)
    file_info = bot.get_file(file_id)
    file_name = file_info.file_path
    downloaded_file = bot.download_file(file_name)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    new_file_name = df2.predict(file_name)
    bot.send_photo(message.chat.id, open(new_file_name, 'rb'))


@bot.message_handler(content_types=['text'])
def message_reply(message):
    log_message(message, message.text)
    bot.send_message(message.chat.id, 'Неизвестная команда')


bot.infinity_polling()
