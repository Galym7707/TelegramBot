import telebot,time, requests, datetime, config, os
#import logging
from background import keep_alive
import pip
from tokens import open_weather_token
from tokens import bot
from pprint import pprint
from codeToSmile import code_to_smile
from aiogram import Bot, types, executor, Dispatcher
#logging.basicConfig(level=logging.INFO)
bot = Bot(token="6097339357:AAG-2fL7KWY-HHzmjvs7n2uh8KLGjI2piNQ", parse_mode="HTML")
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def start(message):
    if message.from_user.last_name != None:
        await message.answer(
        f'Hello, baby! Oh, I mean <b><u>{message.from_user.first_name}</u></b> <b>{message.from_user.last_name}</b>\n'
        f'Сәлем, сәби! (?) Өй, <b><u>{message.from_user.first_name}</u></b> <b>{message.from_user.last_name}</b>'
        )
    else:
        await message.answer(
        f'Hello, baby! Oh, I mean <b><u>{message.from_user.first_name}</u></b>\n'
        f'Сәлем, сәби! (?) Өй, <b><u>{message.from_user.first_name}</u></b>')
    await message.answer('There are some additional commands that you can use now:\n'
                         'Қазір пайдалануға болатын кейбір қосымша командалар бар:\n'
                         '/owner, /help, /website, /weather')


@dispatcher.message_handler(commands=["help"])
async def start1(message):
    await message.reply(
        "Write a city if you want to know its weather or a student, if you want his/her photo. But I warn you, there are few students photo that I have\n"
        "===================================================\n"
        "Ауа-райын білгіңіз келсе қаланы, фотосын алғыңыз келсе студентті жазыңыз. Бірақ ескертемін, менде студенттердің суреттері көп емес"
    )

@dispatcher.message_handler(commands=['website'])
async def website(message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.InlineKeyboardButton("Go to website\n    Веб-сайтқа өту", url="https://fmalmnis.edupage.org/timetable/"))
    await message.reply("Almaty NIS PhM's schedule\nАлматы ФМБ НЗМ сабақ кестесі", reply_markup=markup)


@dispatcher.message_handler(commands=['owner'])
async def owner(message):
    markup_web = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    instagram = types.KeyboardButton("Instagram of the developer\nБот жазған адамның Instagram аккаунты")
    telegram = types.KeyboardButton("Telegram of the developer\nБот жазған адамның Telegram аккаунты")
    markup_web.add(instagram, telegram)
    await message.reply("Go to the social media account of the bot developer:\n"
                        "Бот әзірлеушісінің әлеуметтік медиа аккаунтына өткіңіз келсе:", reply_markup=markup_web)
    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Kumalai", reply_markup=None)
    # bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text="Savesta")

@dispatcher.message_handler(commands=["weather"])
async def show_weather(message: types.Message):
    await message.answer("Write a name of the city to find out its weather\nАуа-райын білу үшін қаланың атын жазыңыз")

@dispatcher.message_handler(content_types=['text'])
async def get_weather(message: types.Message):
    if message.text.lower() == "hello":
        await message.reply("I already said it to you")
    elif message.text.lower() == "сәлем":
        await message.reply("Қайтадан сәлем")
    elif message.text.lower() == "id":
        await message.reply(f"Your ID  is <u>{message.from_user.id}</u>\n"
                            f"Сіздің ID-іңіз <u>{message.from_user.id}</u>")
    elif message.text.lower() == "instagram of the developer\nбот жазған адамның instagram аккаунты":
        markup_inst = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_inst.add(
            types.InlineKeyboardButton("Link my developer's Inst account\nМенің әзірлеушінің Inst парақшасына сілтеме",
                                       url="https://www.instagram.com/edigeev_07/?hl=ru"))
        photo_icon_inst = open("instlogo.jpg", 'rb')
        await message.reply_photo(photo_icon_inst, reply_markup=markup_inst)
    elif message.text.lower() == "telegram of the developer\nбот жазған адамның telegram аккаунты":
        markup_tg = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_tg.add(types.InlineKeyboardButton(
            "Link my developer's account @kemmeq\nМенің әзірлеушінің парақшасына сілтеме @kemmeq",
            url="https://t.me/Kemmeq"))
        photo_icon_telegram = open("telegicon.png", 'rb')
        await message.reply_photo(photo_icon_telegram, reply_markup=markup_tg)
    elif message.text.lower() == "tsoy timur":
        photo_tsoy = open('tsoytimur.jpg', 'rb')
        photo1_tsoy = open('tsoytimur1.jpg', 'rb')
        await message.answer_photo(photo_tsoy)
        await message.answer_photo(photo1_tsoy)
    elif message.text.lower() == "цой тимур":
        photo_tsoy = open('tsoytimur.jpg', 'rb')
        photo1_tsoy = open('tsoytimur1.jpg', 'rb')
        await message.answer_photo(photo_tsoy)
        await message.answer_photo(photo1_tsoy)
    else:
        try:
            request = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )
            data = request.json()
            pprint(data)
            city = data["name"]
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                weather_d = code_to_smile[weather_description]
            else:
                weather_d = "I don't understand what weather is outside \U0001F614\nМен далада қандай ауа-рай екенін түсінбей тұрмын\U0001F614"
            country = data['sys']['country']
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_time = datetime.fromtimestamp(data["sys"]["sunset"])
            sunset_time = datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.fromtimestamp(data["sys"]["sunrise"])
            feels_like = data["main"]["feels_like"]
            # markup_web = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # instagram = types.KeyboardButton("Instagram of the developer\nБот жазған адамның Instagram аккаунты")
            # telegram = types.KeyboardButton("Telegram of the developer\nБот жазған адамның Telegram аккаунты")
            # markup_web.add(instagram, telegram)
            # await message.reply("Go to the social media account of the bot developer:\n"

            markup_lang = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # eng = types.KeyboardButton("beleberda")
            # kz = types.KeyboardButton("xyinya")
            # markup_lang.add(eng, kz)
            # await message.reply("Get info in English\nАқпаратты Қазақ тілінде алу", reply_markup=markup_lang)
            # if message.text.lower() == "beleberda":
            #     await message.answer(
            #         f"Country : {country}\n"
            #         f"Temperature: {cur_weather}°C\nFeels like : {feels_like}°C\n{weather_d}\n"
            #         f"Humidity : {humidity}%\nPressure : {pressure} mm.Hg\nWind : {wind}m/s\n"
            #         f"Sunrise time : {sunrise_time}\nSunset time : {sunset_time}\nLength of one day: {length_of_the_day}\n"
            #     )
            # elif message.text.lower() == "xyinya":
            #     await message.answer(
            #         f"Country : {country}\n"
            #         f"Temperature: {cur_weather}°C\nFeels like : {feels_like}°C\n{weather_d}\n"
            #         f"Humidity : {humidity}%\nPressure : {pressure} mm.hg\nWind : {wind}m/s\n"
            #         f"Sunrise time : {sunrise_time}\nSunset time : {sunset_time}\nLength of one day: {length_of_the_day}\n"
            #     )
            await message.answer(
                f"City : {city}\nCountry : {country}\n"
                f"Temperature: {cur_weather}°C\nFeels like : {feels_like}°C\n{weather_d}\n"
                f"Humidity : {humidity}%\nPressure : {pressure} mm.Hg\nWind : {wind}m/s\n"
                f"Sunrise time : {sunrise_time}\nSunset time : {sunset_time}\nLength of one day: {length_of_the_day}\n"
            )
        except:
            await message.reply("\U00002620 Check the name of the city or student \U00002620\n"
                            "\U00002620 Қаланың немесе студенттің атын тексеріңіз \U00002620")
            await message.answer("\U0001F92B Available student list: Tsoy Timur \U0001F92B\n"
                             "\U0001F92B Қолжетімді студенттер тізімі: Цой Тимур \U0001F92B")



# async def main():
#     city = input("Enter your city: ")
#     get_weather(city, open_weather_token)


if __name__ == '__main__':
    executor.start_polling(dispatcher)

@dispatcher.message_handler(content_types=['photo'])
async def get_user_photo(message):
    await message.reply("What a wonderful photo! What else can I say?")
    await message.reply("Қандай керемет фото! Тағы не айта аламын?")


@dispatcher.message_handler(content_types=['document'])
async def get_user_photo(message):
    await message.reply("Doc? Nevertheless, thank you.")
    await message.reply("Документ? Дегенмен, рахмет.")
keep_alive()
#bot.polling(none_stop= True)