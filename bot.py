import telebot
import config
import  AI

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот который проведёт тебе опрос на тему будующей профессии.")


@bot.message_handler(content_types=["text"])
def echo_message(message):
    bot.reply_to(message, AI.gpt(message.text), parse_mode='Markdown')


bot.infinity_polling()