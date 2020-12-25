from PIL import Image, ImageOps
from pylibdmtx.pylibdmtx import encode
from os import listdir, mkdir
from datetime import datetime
from PIL import ImageDraw
from PIL import ImageFont


def check_barcode_csv_errors(filename: str):
    with open(filename) as file_handler:
        for i, line in enumerate(file_handler, 1):
            if len(line) != 130 and line[-3:-1] != '=':
                print('INVALID line: ', i, ' data: ', line)


def get_barcode_image_from_text(text: str) -> Image:
    encoded = encode(text.encode('utf8'))
    return Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)


def create_dir_and_get_name(prefix: str):
    name = f'{prefix}_{datetime.now()}'
    mkdir(name)
    return name


def concat_images_horizontally(image1: Image, image2: Image):
    dst = Image.new('RGB', (image1.width + image2.width, image1.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (image1.width, 0))
    return dst


def concat_images_vertical(image1: Image, image2: Image):
    dst = Image.new('RGB', (image1.width, image1.height + image2.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (0, image1.height))
    return dst


def add_black_space_around_image(image: Image, border=1):
    return ImageOps.expand(image, border=border, fill='black')


def add_white_space_around_image(image: Image, border=1):
    return ImageOps.expand(image, border=border, fill='white')


def get_barcode_text_image(width, border, barcode_text):
    font_size = 13
    font = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", font_size)

    image = Image.new("RGB", (width, (font_size * 2 + 2)), 'white')
    draw = ImageDraw.Draw(image)
    draw.text(
        (border - 5, 0),
        barcode_text[:15] + '\n' + barcode_text[16:31],
        font=font,
        fill='black',
        align='center',
        spacing=-1
    )
    return image
