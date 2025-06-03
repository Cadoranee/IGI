import requests
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger('insurance_app')

def get_weather(city):
    """
    Получение данных о погоде через OpenWeatherMap API
    """
    try:
        params = {
            'q': city,
            'appid': settings.OPENWEATHERMAP_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        
        print(f"Отправка запроса к API погоды с параметрами: {params}")
        response = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=params)
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Ошибка API: {response.json()}")
            return None
            
        data = response.json()
        # Берем данные о погоде на текущий момент (первый элемент в списке)
        current_weather = data['list'][0]
        weather_data = {
            'temperature': round(current_weather['main']['temp']),
            'description': current_weather['weather'][0]['description'],
            'icon': current_weather['weather'][0]['icon']
        }
        print(f"Получены данные о погоде: {weather_data}")
        return weather_data
    except Exception as e:
        print(f"Ошибка при получении данных о погоде: {str(e)}")
        return None

def get_exchange_rates():
    """
    Получение курсов валют через Exchange Rates API
    """
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        response.raise_for_status()
        
        data = response.json()
        return {
            'USD': data['rates']['USD'],
            'EUR': data['rates']['EUR'],
            'RUB': data['rates']['RUB']
        }
    except Exception as e:
        logger.error(f'Ошибка при получении курсов валют: {str(e)}')
        return None

def convert_currency(amount, from_currency, to_currency):
    """
    Конвертация валют
    """
    try:
        rates = get_exchange_rates()
        if rates:
            # Конвертируем через USD как базовую валюту
            if from_currency != 'USD':
                amount_in_usd = amount / rates['rates'][from_currency]
            else:
                amount_in_usd = amount
                
            if to_currency != 'USD':
                converted_amount = amount_in_usd * rates['rates'][to_currency]
            else:
                converted_amount = amount_in_usd
                
            return round(converted_amount, 2)
        return None
    except Exception as e:
        print(f"Ошибка при конвертации валют: {e}")
        return None 