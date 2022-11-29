import telebot
from telebot.util import extract_arguments, extract_command, is_command

import config
import calculator
import tick_tack_toe

API_TOKEN = config.token
NEW_GAME = None
ARROW_SYMBOL = '\u2198'

bot = telebot.TeleBot(API_TOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand('start', 'начало работы'),
        telebot.types.BotCommand('calc', 'использовать калькулятор'),
        telebot.types.BotCommand('game', 'играть в крестики-нолики')
    ],
)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Готов к работе!')


@bot.message_handler(commands=['calc'])
def calc_message(message):
    if extract_arguments(message.text):
        process_expression(message)
    else:
        msg = bot.reply_to(message, f'Введите выражение для вычисления {ARROW_SYMBOL}')
        bot.register_next_step_handler(msg, process_expression)


def process_expression(message):
    expr = extract_arguments(message.text) if is_command(message.text) else message.text
    text_result = str(calculator.get_result(expr)).replace('.', ',').removesuffix(',0')
    bot.send_message(message.chat.id, f'{expr} = {text_result}')


def show_game_field(lst):
    return '\n'.join([''.join(row) for row in lst])


@bot.message_handler(commands=['game'])
def game_message(message):
    global NEW_GAME
    if not NEW_GAME:
        NEW_GAME = tick_tack_toe.Game()
    process_game(message)


def process_game(message):
    if NEW_GAME.winner:
        reply = f'{show_game_field(NEW_GAME.buttons)}\n' \
                f'{NEW_GAME.winner_text}'
        NEW_GAME.restart_game()
        bot.send_message(message.chat.id, reply)
    else:
        reply = f'{show_game_field(NEW_GAME.buttons)}\n' \
                f'Введите номер ряда (1-3) и столбца (1-3) через пробел {ARROW_SYMBOL}'
        msg = bot.send_message(message.chat.id, reply)
        bot.register_next_step_handler(msg, process_next_move)


def process_next_move(message):
    if is_command(message.text):
        for handler in bot.message_handlers:
            if extract_command(message.text) in handler['filters']['commands']:
                handler['function'](message)
                return

    move = message.text.split()

    if len(move) != 2:
        msg = bot.reply_to(message, 'Неверный формат ввода, введите 2 числа через пробел.')
        bot.register_next_step_handler(msg, process_next_move)
        return

    try:
        i, j = map(int, move)
    except ValueError:
        msg = bot.reply_to(message, 'Неверный формат ввода, вводите только целые числа.')
        bot.register_next_step_handler(msg, process_next_move)
        return

    if i not in range(1, 4) or j not in range(1, 4):
        msg = bot.reply_to(message, 'Значения за пределами поля, вводите только числа от 1 до 3.')
        bot.register_next_step_handler(msg, process_next_move)
        return

    i -= 1
    j -= 1
    if (i, j) not in NEW_GAME.available_buttons:
        msg = bot.reply_to(message, 'Поле уже занято, попробуйте ещё раз.')
        bot.register_next_step_handler(msg, process_next_move)
        return

    NEW_GAME.toggle_field(i, j)
    process_game(message)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    bot.send_message(message.chat.id, 'Неизвестная команда')


bot.infinity_polling()
