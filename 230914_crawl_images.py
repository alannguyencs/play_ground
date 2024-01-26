import os, shutil
from tqdm import tqdm
from icrawler.builtin import GoogleImageCrawler
def gen_dir(new_dir, remove_old=False):
    if remove_old:
        if os.path.exists(new_dir):
            for file_name in os.listdir(new_dir):
                file_path = os.path.join(new_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(e)
        else:
            os.mkdir(new_dir)


    elif not os.path.exists(new_dir):
        os.mkdir(new_dir)

    return (new_dir + '/')


def crawl_images_major_keys():
    image_dir = "/media/alan/新增磁碟區/toshiba/cairs/emma/images/"

    major_key_file = list(open('image_key.txt', 'r'))
    for id, line in tqdm(enumerate(major_key_file)):
        print("{}/{}: {}".format(id, len(major_key_file), line))
        key = line.strip()
        search_description = f"{key}"
        raw_dir = gen_dir("{}{}".format(image_dir, key))
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,
                                            storage={'root_dir': raw_dir})
        google_crawler.crawl(keyword=search_description, max_num=256,
                             min_size=(256, 256), max_size=None)

if __name__=='__main__':
    crawl_images_major_keys()