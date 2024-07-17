import json
import requests
from values import VALUES



class DataValidationException(Exception):
    pass


class Converter():
    @staticmethod

    def convert(base: str, quote: str, base_amount: str) -> str:

        try:
            base_key = VALUES[base.lower()]
        except KeyError:
            e = f'Ошибка!!!\n Указанная вами валюта {base} не найдена.'
            raise DataValidationException(e)

        try:
            quote_key = VALUES[quote.lower()]
        except KeyError:
            e = f'Ошибка!!!\n Указанная вами валюта {base} не найдена.'
            raise DataValidationException(e)

        if base_key == quote_key:
            e = f'Ошибка!!!\n Невозможно конвертировать одинаковые валюты.'
            raise DataValidationException(e)

        try:
            base_amount = float(base_amount.replace(',', '.'))
        except ValueError:
            e = f'Ошибка!!!\n Неудалось обработать количество {base_amount}.'
            raise DataValidationException(e)

        url = (f'https://https://api.apilayer.com/currency_data/convert?to={base_key}&from={quote_key}&amount={base_amount}')
        headers = {
            "apikey": "EVHQMG9HEYCfbtz7IjmAkWNJ5ZGPkzr5"
        }
        response = requests.request("GET", url, headers=headers)
        result = response.text
        data = json.loads(response.content)

        quote_amount = round(data, result, 2)
        return f'{base_amount:.2f} {base_key} → {quote_amount} {quote_key}'




