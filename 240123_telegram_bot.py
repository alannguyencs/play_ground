import secret
import requests
import datetime
import time

import telebot
from deep_translator import GoogleTranslator


TRANSLATION_ERROR = "Translation error. Please try again later."
translator = GoogleTranslator(source='en', target='vi')
def translate(text):
    num_try = 10
    while num_try > 0:
        try:
            return translator.translate(text)
        except:
            num_try -= 1
            time.sleep(1)
            pass
    # return translator.translate(text)
    return TRANSLATION_ERROR

bot = telebot.TeleBot(secret.apiToken)  # replace "api" with your bot's API token

@bot.message_handler(content_types=['text'])
def welcome(message):
    sent_msg = bot.send_message(message.chat.id, "Welcome to the bot. What's your name?")
    bot.register_next_step_handler(sent_msg, translate_handler)  # Next message will call the name_handler function

def name_handler(message):
    name = message.text
    sent_msg = bot.send_message(message.chat.id, f"Your name is {name}. How old are you?")
    bot.register_next_step_handler(sent_msg, age_handler, name)  # Next message will call the age_handler function

def age_handler(message, name):
    age = message.text
    bot.send_message(message.chat.id, f"Your name is {name}, and your age is {age}.")

def translate_handler(message):
    user_text = message.text
    try:
        sent_msg = bot.send_message(message.chat.id, translate(user_text))
    except:
        sent_msg = bot.send_message(message.chat.id, TRANSLATION_ERROR)
        pass
    bot.register_next_step_handler(sent_msg, translate_handler)

bot.polling()