import telebot

from bot_const import TOKEN, keys_RU
from util_bot import Convert_Exception, Currency_Convert

from cx_Freeze import ConfigError

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты котоую необходимо пересте в ЕВРО>' \
           '\ <количество переводимой валюты> \n Увидеть список всех доступных валют - /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys_RU.keys():
       text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def row_text(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) > 2:
            raise Convert_Exception(f'Слишком много параметров.')
        elif len(values) < 2:
            raise Convert_Exception(f'Слишком мало параметров.')

        quote, amount = values

        text_response = Currency_Convert.convert(quote, amount)
    except Convert_Exception as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, text_response)

bot.polling(none_stop=True)