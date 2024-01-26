import secret
import requests
import datetime
import time
import easyocr

import telebot
from io import BytesIO
from deep_translator import GoogleTranslator
from alutils import alos, alimage
from PIL import Image
import glob
#===================================================================================================
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Initialize the ChatOpenAI with your API key and optional organization ID
chat = ChatOpenAI(temperature=0, openai_api_key=secret.openai_api_key, 
                  openai_organization=secret.openai_organization)

def get_chinese_dish(text):
    prompt = f"You are a helpful assistant that understand Chinese and food.\n\
                Split the following text to extract Chinese dishes.\
                Each dish is written in Chinese and separated by a line.\n\
                On each line, write the dish in Chinese, then a comma, then the English translation\
                    then a comma, then the Vietnamese translation.\n\
                Text: {text}\n\""
    # Send the prompt to the chat model and get the response
    response = chat([SystemMessage(content=prompt)])
    print (text, response.content)
    return response.content.split('\n')

#===================================================================================================
from icrawler.builtin import GoogleImageCrawler

def form_image(image_dir):
    image_paths = glob.glob(f"{image_dir}*")
    images = []
    for image_path in image_paths:
        print (image_path)
        try:
            image = Image.open(image_path).resize((256, 256), Image.LANCZOS)
            images.append(image)
        except Exception as e:
            print (e)
            pass
    if len(images) == 0:
        return None
    full_image = alimage.stack_images(images[:4], direction='HORIZONTAL')
    return full_image

def crawl_image(keyword, prefix='香港食品: '): #Hong Kong food
    image_dir = alos.gen_dir(f'data/image/{keyword}')
    google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, 
                                        storage={'root_dir': image_dir})
    google_crawler.crawl(keyword=prefix + keyword, 
                         max_num=10, min_size=(256, 256), max_size=None)
    vis_image = form_image(image_dir)
    return vis_image


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

def image_to_text(image_path):
    reader = easyocr.Reader(['ch_tra'])
    result = reader.readtext(image_path)
    texts = [result[i][-2] for i in range(len(result))]
    for i, text in enumerate(texts):
        print (i, text)
    return texts


bot = telebot.TeleBot(secret.apiToken)  # replace "api" with your bot's API token

# Handler for text messages
@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Process the text message
    bot.reply_to(message, "You sent text: " + message.text)

# Handler for images/photos
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Process the photo message
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    #get datetime to yymmdd_hhmmss
    now = datetime.datetime.now()
    dt_string = now.strftime("%y%m%d_%H%M%S")
    image_path = f"data/image/{dt_string}.jpg"
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    texts = image_to_text(image_path)
    chinese_dishes = get_chinese_dish(texts)
    chinese_dishes = [dish for dish in chinese_dishes if dish.count(',') == 2]
    # text_dishes = [text for text in texts if is_a_dish(text)]
    # text_dishes = [text for text in texts]
    for i, dish in enumerate(chinese_dishes):
        print (i, dish)
    if chinese_dishes and len(chinese_dishes) > 0:
        # crawl_image(text_dishes[0])
        # response = '\n'.join(chinese_dishes)
        for dish in chinese_dishes:
            bot.reply_to(message, dish)
            vis_image = crawl_image(dish.split(',')[0])
            bio = BytesIO()
            bio.name = 'data/image.jpeg'
            vis_image.save(bio, 'JPEG')
            bio.seek(0)
            bot.send_photo(message.chat.id, photo=bio)
    else:
        response = "No dish found."
        bot.reply_to(message, response)

# Polling
bot.polling()