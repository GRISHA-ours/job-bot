import telebot
import config

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот который проведёт тебе опрос на тему будующей профессии.")


@bot.message_handler(content_types=["text"])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()