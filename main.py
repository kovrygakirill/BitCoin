import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from rate_bitcoin import get_rate_bitcoin_for_button, get_rate_bitcoin_for_calendar
from rate_bitcoin import TYPE_TIMEDELTA

from my_eception import SendShitException
from validator import check_valid_for_calendar

BOT = telebot.TeleBot('5129685023:AAFpZCDJa1YRGDRdbZ-xmI312ZCrGhRwuX8')
CHAT_ID_ADMIN = 436913550


@BOT.message_handler(commands=['start'])
def start_main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[types.KeyboardButton(type_d) for type_d in TYPE_TIMEDELTA])

    send_mess = f"Hello, {message.from_user.first_name}.\nDo you need help? click /help"
    BOT.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAIB5GIsoSox-LsyWJoHheCTc9FnibTDAAIOAAN0nKkWZZPmmrj9EG4jBA')
    BOT.send_message(message.chat.id, send_mess, parse_mode="html", reply_markup=markup)

    send_msg_for_admin(message)


@BOT.message_handler(commands=['help'])
def start_help(message):
    send_mess = f"If you want to know the exchange rate of Bitcoin, " \
                f"click the buttons below.\nif you want to know the rate on a particular day, write date in format " \
                f"YYYY-MM-DD or click /calendar and select day."
    BOT.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAIB5mIsoUmoC9lrpZJFEmXOFZJc_8o-AAKBFQAC6-BRSA2liECjqYknIwQ')
    BOT.send_message(message.chat.id, send_mess, parse_mode="html")


@BOT.message_handler(commands=['calendar'])
def start_calendar(message):
    calendar, step = DetailedTelegramCalendar().build()
    BOT.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAICDGIspI5XRyespzkP-4V63ldmMatwAAIbAwACbbBCAx-vcfH7DgxKIwQ')
    BOT.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@BOT.callback_query_handler(func=DetailedTelegramCalendar.func())
def call_calendar(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        BOT.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        BOT.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)

        try:
            bit_rate = get_rate_bitcoin_for_calendar(str(result))
        except SendShitException:
            BOT.send_sticker(
                c.message.chat.id,
                sticker='CAACAgIAAxkBAAIB6GIsoZWk5IDGBp4GudyrpKq5FnoKAAItAQACWQMDAAEt9hslJkzrsSME')
            return

        final_mess = f"{result} Bitcoin rate = {'-' if bit_rate is None else bit_rate} $"
        BOT.send_sticker(c.message.chat.id,
                         sticker='CAACAgIAAxkBAAIB9mIsoqg-PObVyh08eSdu-S_iGQ8MAALcGAACK28hSZC5lRItLClAIwQ')
        BOT.send_message(c.message.chat.id, final_mess, parse_mode="html")


@BOT.message_handler(content_types=['text'])
def process_text(message):
    message_user = message.text.strip().lower()
    try:
        valid_msg_calendar = check_valid_for_calendar(message_user)
        if valid_msg_calendar:
            bit_rate = get_rate_bitcoin_for_calendar(message_user)
        else:
            bit_rate = get_rate_bitcoin_for_button(message_user)
    except SendShitException:
        BOT.send_sticker(
            message.chat.id,
            sticker='CAACAgIAAxkBAAIB6GIsoZWk5IDGBp4GudyrpKq5FnoKAAItAQACWQMDAAEt9hslJkzrsSME')
        return

    final_mess = f"{message_user} Bitcoin rate = {bit_rate} $"
    BOT.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAIB9GIsolRj6QcwbtsmYKAhOpxgMdzzAAKAGAACj2rISNRGejv7n_wfIwQ')
    BOT.send_message(message.chat.id, final_mess, parse_mode="html")


@BOT.message_handler(content_types=['sticker'])
def process_text(message):
    file_info = message.sticker.file_id
    print(file_info)
    BOT.send_sticker(message.chat.id,
                     sticker='CAACAgIAAxkBAAIB6GIsoZWk5IDGBp4GudyrpKq5FnoKAAItAQACWQMDAAEt9hslJkzrsSME')


def send_msg_for_admin(message):
    if message.chat.id == CHAT_ID_ADMIN:
        return

    msg_for_admin = f"Somebody run your bot: Name - {message.from_user.first_name}, " \
                    f"Last_name - {message.from_user.last_name}, " \
                    f"username - {message.from_user.username}"
    BOT.send_sticker(CHAT_ID_ADMIN, sticker='CAACAgIAAxkBAAICzWIvTTYGaRSjvZT2Dldt86dtu_MWAAIkEQACfsZ5SGES9vQGgHdtIwQ')
    BOT.send_message(CHAT_ID_ADMIN, msg_for_admin, parse_mode="html")


try:
    BOT.polling(none_stop=True)
except Exception as ex:
    BOT.send_sticker(CHAT_ID_ADMIN, sticker="CAACAgIAAxkBAAICZWIvRiZN5zthCwTXwKZ8DKEWctVwAAI4EQACe2KYScU9o5OriGzxIwQ")
    BOT.send_message(CHAT_ID_ADMIN, f"'{type(ex).__name__}' - {ex}", parse_mode="html")
    BOT.polling(none_stop=True)
