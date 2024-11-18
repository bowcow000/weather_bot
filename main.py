#pip install pyTelegramBotAPI requests

import logging
import requests
import telebot

API_TOKEN = 'TOKEN'
OPENWEATHER_API_KEY = '69357a395658a1d57bd421d8e7cba196'

bot = telebot.TeleBot(API_TOKEN)

def get_weather_samara():
    city = "Самара"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"❌ Ошибка при запросе данных: {e}"

    if response.status_code == 200:
        data = response.json()

        if 'main' in data and 'weather' in data and 'wind' in data:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            weather_desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            country = data['sys']['country']

            return (
                f"🌤 Погода в {city_name}, {country}:\n"
                f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                f"Описание: {weather_desc}\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с"
            )
        else:
            return '❌ Не удалось получить полные данные о погоде.'
    else:
        return '❌ Не удалось получить данные о погоде.'


@bot.message_handler(commands=['start'])
def cmd_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = telebot.types.KeyboardButton("Погода в Самаре")
    markup.add(button)

    bot.send_message(
        message.chat.id,
        "Привет! Я погодный бот.",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def cmd_help(message):
    help_text = (
        "/start - Запуск бота\n"
        "/help - Получить помощь\n"
        "Нажмите на кнопку ниже для получения погоды."
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: message.text == "Погода в Самаре")
def process_weather_samara(message):
    weather = get_weather_samara()
    bot.send_message(message.chat.id, weather)

if __name__ == '__main__':
    bot.polling(none_stop=True)
