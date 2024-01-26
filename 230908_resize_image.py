from PIL import Image

image_dir = "/home/alan/GoogleDrive/Detalytics/avatar/report/images"
image_name = 'age'
extention = '.png'

image = Image.open(f"{image_dir}/{image_name}{extention}")
image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))
image.save(f"{image_dir}/{image_name}_resized{extention}")