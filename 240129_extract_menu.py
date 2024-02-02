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
import cv2
from datetime import datetime
from collections import OrderedDict

def get_datetime():
    return datetime.now().strftime("%y%m%d_%H%M%S_%f")

class MenuExtractor:
    def __init__ (self, video_path):
        #step 1: split video to frames, and extract text from each frame
        self.reader = easyocr.Reader(['ch_tra'])
        time_ = datetime.now().strftime("%y%m%d")
        self.data_path = alos.gen_dir(f"data/menu/{time_}")
        self.extract(video_path)

    def extract(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_cnt = 1
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                print (frame_cnt)
                texts = self.reader.readtext(frame)
                # for text in texts:
                #     print (text)
                texts = [result[-2] for result in texts if result[-1] > 0.5]
                log_file = open(f"{self.data_path}{frame_cnt}.txt", "w")
                log_file.write('\n'.join(texts))
                log_file.close()
                frame_cnt += 1
            else:
                break


class DATABASE:
    def __init__(self):
        self.data_path = "data/menu/"
        # self.concatenate()
        # self.get_dishes()
    
    def get_dishes(self, folder_name='240129'):
        data = glob.glob(f"{self.data_path}{folder_name}/*.txt")
        category = {}
        dishes = {}
        for file in tqdm(data):
            file_id = int(alos.get_file_name(file))
            file = list(open(file, "r"))
            for line_id, line in enumerate(file):
                if line_id < len(file) - 2 and file[line_id+1][0] != '$' and file[line_id+2][0] == '$':
                    category_log = file_id * 1000000 + line_id
                    category_ = line.strip()
                    category[category_] = category_log

                if line_id < len(file) - 1 and file[line_id][0] != '$' and file[line_id+1][0] == '$':
                    dish_log = file_id * 1000000 + line_id
                    dish = line.strip()
                    if dish not in dishes:
                        dishes[dish] = {
                            'dish_log': dish_log,
                            'price': file[line_id+1].strip(),
                        }
                    else:
                        dishes[dish]['dish_log'] = dish_log
        
        #orders
        orders = []
        for key, pos in category.items():
            orders.append((pos, key))
        # for key, pos in dishes.items():
        #     orders.append((pos['dish_log'], key))
        orders.sort()
        for order in orders:
            print (order[1])
        # dish_file = open(f"{self.data_path}/{folder_name}_dishes.txt", "w")
        # for _, name in orders:
        #     dish_file.write(f"{name}\n")
        #     if name in dishes:
        #         dish_file.write(f"{dishes[name]['price']}\n")
        # dish_file.close()
            
    def concatenate(self, folder_name='240129'):
        data = sorted(glob.glob(f"{self.data_path}{folder_name}/*.txt"))
        texts = []
        for file in data[:-1]:
            texts += list(open(file, "r"))
        #write to file
        file = open(f"{self.data_path}{folder_name}/all.txt", "w")
        file.write(''.join(texts))
        file.close()





# menu_extractor = MenuExtractor("data/menu/RPReplay_Final1706512646.MP4")
database = DATABASE()
database.concatenate()
