# подключение библиотек
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: вставить свой токен
TOKEN = '6217533975:AAEHirOf6ATuiTtah7ai8RpBJl9qk7zxmiY'
bot = TeleBot(TOKEN, parse_mode='html')
# утилита для генерации номеров кредитных карт
# указываем язык - русский
faker = Faker('ru_RU') 

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей. "\
        "Напиши сколько пользователей тебе нужно 👇🏻",
        #reply_markup=main_menu_reply_markup
    )


# обработчик всех остальных сообщений
@bot.message_handler(content_types=['text'])
def message_handler(message):

    users_cnt = int(message.text)
    # определяем количество тестовых пользователей
    # или отправляем ошибку    
    payload_len = 0

    if type(users_cnt) == int:
        payload_len = users_cnt
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь ввести еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
