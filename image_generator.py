from PIL import Image
from urllib.parse import urlparse
import os
import re
import random

downloaded_images_directory = '/Users/slaza/PycharmProjects/renamer/image_generation/images'  # your directory
downloaded_images = os.listdir(downloaded_images_directory)
current_directory = os.getcwd()
pattern = re.compile(r'\d{3,4}x\d{3,4}')


def image_paths(image):
    url = urlparse(image)
    file_path = url.path.split('/')
    file_name = file_path[-1]
    file_path = '/'.join(file_path[:-1]) + '/'
    return file_name, file_path


def get_dimensions_from_name(file_name):
    match = re.findall(pattern, file_name)
    if match:
        return tuple([int(x) for x in match[0].split('x')])
    else:
        return 300, 400  # Your dimentions


def image_processing(broken_dimensions, file_path, file_name):
    donor_image = random.choice(downloaded_images)
    original = Image.open(downloaded_images_directory + '/' + donor_image)
    width, height = original.size   # Get dimensions
    left = width/4
    top = height/4
    right = 3 * width/4
    bottom = 3 * height/4
    cropped = original.crop((left, top, right, bottom))
    cropped.thumbnail(broken_dimensions, Image.ANTIALIAS)
    cropped.save(current_directory + '/image_generation' + file_path + file_name, "JPEG")
    return None


if __name__ == '__main__':
    with open('image_generation/broken_images', 'r') as f:
        broken_images = f.read().split('\n')

    for broken_image in broken_images:
        name, path = image_paths(broken_image)
        if not os.path.exists(current_directory + '/image_generation' + path):
            os.makedirs(current_directory + '/image_generation' + path)
        dimensions = get_dimensions_from_name(name)
        image_processing(dimensions, path, name)





