import secret
import datetime
import time
import easyocr
import os
import telebot
from io import BytesIO
from tqdm import tqdm
from alutils import alos, alimage
from PIL import Image, ImageDraw, ImageFont
import glob
import multiprocessing
#===================================================================================================
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Initialize the ChatOpenAI with your API key and optional organization ID
chat = ChatOpenAI(temperature=0, openai_api_key=secret.openai_api_key, 
                  openai_organization=secret.openai_organization)

def is_a_dish(text):
    prompt = f"You are a helpful assistant that understand Chinese and food and drink.\n\
                Is the following text a dish or a drink?\n\
                Return 1 if true, 0 if false.\n\
                Text: {text}\n\""
    response = chat([SystemMessage(content=prompt)])
    return response.content == '1'

def get_chinese_dish(text):
    prompt = f"You are a helpful assistant that understand Chinese and food and drink.\n\
                Split the following text to extract Chinese dishes.\
                Each dish is written in Chinese and separated by a line.\n\
                On each line, write the dish in Chinese, then a comma, then the English translation\
                    then a comma, then the Vietnamese translation.\n\
                Text: {text}\n\""
    # Send the prompt to the chat model and get the response
    response = chat([SystemMessage(content=prompt)])
    dishes = response.content.split('\n')
    dishes = [dish.replace('/', '或') for dish in dishes if is_a_dish(dish)]
    return dishes

#===================================================================================================
from icrawler.builtin import GoogleImageCrawler

def form_image(image_dir):
    print (image_dir)
    image_paths = glob.glob(f"{image_dir}/*")
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
    first_image = alimage.stack_images(images[:4], direction='HORIZONTAL')
    second_image = alimage.stack_images(images[-4:], direction='HORIZONTAL')
    w, h = first_image.size
    full_image = alimage.stack_images([first_image, second_image], 
                                      unit_w=w, unit_h=h, direction='VERTICAL')
    return full_image

def put_text_on_image(image, text):
    text = text.replace(',', '\n')
    unit_size = 256
    gap = 16
    pos_x, pos_y = 32, 32
    full_image = Image.new('RGB', (unit_size * 4 + gap * 3, 
                                   unit_size * 3 + gap), (255, 255, 255))
    full_image.paste(image, (0, unit_size))
    img_draw = ImageDraw.Draw(full_image)
    font = ImageFont.truetype('data/NotoSans.ttf', size=40)
    encoded_text = text.encode('utf-8')
    img_draw.text((pos_x, pos_y), encoded_text.decode('utf-8'), fill='black', font=font)
    return full_image


def crawl_image(keyword, prefix='香港食品: '): #Hong Kong food
    folder_name = '_'.join(keyword.split(',')[:2]) #get chinese and english name
    image_dir = f'data/image/{folder_name}'
    print (image_dir, os.path.isdir(image_dir))
    if not os.path.isdir(image_dir):
        os.makedirs(image_dir)
        chinese_keyword = keyword.split(',')[0]
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, 
                                            storage={'root_dir': image_dir})
        google_crawler.crawl(keyword=prefix + chinese_keyword, 
                            max_num=12, min_size=(256, 256), max_size=None)
    vis_image = form_image(image_dir)
    label_image = put_text_on_image(vis_image, keyword)
    return label_image

def read_text(image_path, queue):
    reader = easyocr.Reader(['ch_tra'])
    result = reader.readtext(image_path)
    queue.put(result)

def image_to_text(image_path):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=read_text, args=(image_path, queue))
    process.start()

    # Wait for 10 seconds or until process finishes
    process.join(10)

    if process.is_alive():
        print("OCR is taking longer than expected. Terminating process...")
        process.terminate()
        process.join()
    
    # Get the result
    if not queue.empty():
        result = queue.get()
        # print(result)

        # reader = easyocr.Reader(['ch_tra'])
        # result = reader.readtext(image_path)
        texts = [result[i][-2] for i in range(len(result))]
        for i, text in enumerate(texts):
            print (i, text)
        return texts
    return []


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
    if len(texts) == 0:
        bot.reply_to(message, "No text found.")
        return
    
    chinese_dishes = get_chinese_dish(texts)
    chinese_dishes = [dish for dish in chinese_dishes if dish.count(',') == 2]

    start_time = time.time()
    if chinese_dishes and len(chinese_dishes) > 0:
        bot.reply_to(message, '\n'.join(chinese_dishes))
        for i, dish in tqdm(enumerate(chinese_dishes)):
            bot.reply_to(message, dish)
            vis_image = crawl_image(dish)
            if vis_image is None:
                continue
            bio = BytesIO()
            bio.name = 'data/image.jpeg'
            vis_image.save(bio, 'JPEG')
            bio.seek(0)
            bot.send_photo(message.chat.id, photo=bio)

            now = time.time()
            #if running time larger than 1 minute: break
            if now - start_time > 60:
                break
    else:
        response = "No dish found."
        bot.reply_to(message, response)

# Polling
bot.polling()