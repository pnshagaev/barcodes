from lib import check_barcode_csv_errors, get_barcode_image_from_text, create_dir_and_get_name, concat_images_vertical, \
    add_white_space_around_image, add_black_space_around_image, get_barcode_text_image

from PIL import Image

IMAGE_WIDTH = 158
BARCODE_BORDER = 25
if __name__ == '__main__':
    filename = 'order_ce5ba19f-11bd-49e5-b113-31023e88ac2b_gtin_02900020018604_quantity_50_2137598815331727890'
    barcodes_csv_filename = f'media/files/{filename}.csv'
    # check_barcode_csv_errors(barcodes_csv_filename)

    with open(barcodes_csv_filename) as file_handler:
        with Image.open('media/images/honest_sign_logo.png') as logo:
            logo.thumbnail((IMAGE_WIDTH, (logo.height / (logo.width / IMAGE_WIDTH))), Image.ANTIALIAS)
            logo = add_white_space_around_image(logo,
                                                         (0, -3, 0, -6))
            dir_name = create_dir_and_get_name(filename)

            for line_number, barcode_text_line in enumerate(file_handler, 1):
                barcode_image = get_barcode_image_from_text(barcode_text_line)
                barcode_image = add_white_space_around_image(barcode_image,
                                                             (BARCODE_BORDER, BARCODE_BORDER, BARCODE_BORDER, -10))
                barcode_image.thumbnail((IMAGE_WIDTH, IMAGE_WIDTH), Image.NEAREST)
                text_image = get_barcode_text_image(IMAGE_WIDTH, BARCODE_BORDER, barcode_text_line)
                barcode_image = concat_images_vertical(barcode_image, text_image)
                barcode_image = concat_images_vertical(barcode_image, logo)
                barcode_image = add_black_space_around_image(barcode_image, 1)
                barcode_image.save(f'{dir_name}/barcode_{line_number}.png')
