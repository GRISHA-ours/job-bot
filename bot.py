import telebot
import config
import  AI
from telebot import types 

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)

# Product prices in stars
PRICES = {
    '1 Stars': 1,   # $1.00 - Entry level package
    '3 Stars': 3,   # $4.50 - Medium package with 10% discount
    '5 Stars': 5,  # $8.00 - Large package with 20% discount
    '10 Stars': 10  # $35.00 - Bulk package with 30% discount
}


@bot.message_handler(commands=['donate'])
def send_donate(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(product) for product in PRICES.keys()]
    markup.add(*buttons)

    bot.reply_to(message, 
                 "Если вам понравился бот задонатьте пожалуйста на еду",
                 reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in PRICES.keys())
def handle_product_selection(message):
    product = message.text
    price = PRICES[product]
    
    prices = [types.LabeledPrice(label=product, amount=price)]
    
    bot.send_invoice(
        message.chat.id,
        title=f"Оплата {product}",  # Title of the invoice
        description=f"Купить {product}",  # Description shown on invoice
        provider_token='',  # Payment provider token (empty for testing)
        currency='XTR',  # Currency code
        prices=prices,  # List of prices (we only have one item)
        start_parameter='stars-payment',  # Deep-linking parameter
        invoice_payload=product  # Payload to identify the product after payment
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Handler for successful payments
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    # Get the product that was purchased from the invoice payload
    product = message.successful_payment.invoice_payload
    bot.reply_to(message, 
                 f"Payment for {product} successful!")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот который проведёт тебе опрос на тему будующей профессии.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Привет, вот полезные комманды для удобной работы с ботом: /help, /start, /donate")


@bot.message_handler(content_types=["text"])
def echo_message(message):
    bot.reply_to(message, AI.gpt(message.text), parse_mode='Markdown')


bot.infinity_polling()