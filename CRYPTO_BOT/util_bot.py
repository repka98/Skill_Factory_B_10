import requests
import json
from bot_const import keys_RU, keys_EN

class Convert_Exception(Exception):
    pass

class Currency_Convert:
    @staticmethod
    def convert(quote: str, amount: str):

        if quote == keys_RU['евро']:
            raise Convert_Exception(f'Невозможно конвертировать одинаковые валюты - Eвро')

        try:
            quote_ticket = keys_RU[quote]
        except KeyError:
            raise Convert_Exception(f'Невозможно обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise Convert_Exception(f'Невозможно обработать количество {amount}')

        rem_amount = amount % 10

        if rem_amount == 1:
            amount_ticket = keys_EN[keys_RU[quote]][0]
        elif 2 <= rem_amount <= 4:
            amount_ticket = keys_EN[keys_RU[quote]][1]
        else:
            amount_ticket = keys_EN[keys_RU[quote]][2]

        answer_dist = {}
        r = requests.get(f'http://data.fixer.io/api/latest?access_key=dc8ccfabd33fc95afb28700865aeb841')
        text = json.loads(r.content)
        rates = text.get('rates')
        r_equal = rates[keys_RU[quote]]
        multi_equal = float(amount) / r_equal
        text_response = f'Курс {int(amount)} {amount_ticket} в Евро - {multi_equal:.2f}'
        return text_response
