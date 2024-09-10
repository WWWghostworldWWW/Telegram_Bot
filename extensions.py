import json
import requests
from values import VALUES

class APIException(Exception):
    pass


class CurrencyConverter:
    currency = VALUES


    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount=float(amount)
        except ValueError:
            raise APIException(f'Неудалось обработать количество {amount}. Введите число!')

        base = CurrencyConverter.currency.get(base.lower(), base.upper())
        quote= CurrencyConverter.currency.get(quote.lower(), quote.upper())

        if base == quote:
            raise APIException(f'Нет смысла переводить одинаковую валюту {base}!')


        url = f'https://v6.exchangerate-api.com/v6/88d9234997a222d0b342cb12/latest/{base}'
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            raise APIException('Не удалось получиить ответ от сервера!')

        rates = data.get('conversion_rates', {})

        if quote not in rates:
            raise APIException(f'Валюта {quote} не найдена!')

        converted_amount = rates[quote] * amount
        return round(converted_amount, 2)




