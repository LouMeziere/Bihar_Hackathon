import os
from PIL import Image

def crop_to_aspect_ratio(img, target_ratio):
    img_width, img_height = img.size
    img_ratio = img_width / img_height

    if img_ratio > target_ratio:
        # Image is wider than target ratio: crop width
        new_width = int(target_ratio * img_height)
        left = (img_width - new_width) // 2
        upper = 0
        right = left + new_width
        lower = img_height
    else:
        # Image is taller than target ratio: crop height
        new_height = int(img_width / target_ratio)
        left = 0
        upper = (img_height - new_height) // 2
        right = img_width
        lower = upper + new_height

    return img.crop((left, upper, right, lower))

input_folder = 'images/arts'
output_folder = 'arts_out'
target_ratio = 4 / 3  # For example, 4:3 aspect ratio; change as needed

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        cropped_img = crop_to_aspect_ratio(img, target_ratio)

        save_path = os.path.join(output_folder, filename)
        cropped_img.save(save_path)

        print(f'Cropped to {target_ratio:.2f} and saved: {save_path}')
