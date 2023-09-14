from PIL import Image
import os
from tqdm import tqdm


def compress_images(folder_path, output_path, quality=90):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    image_files = os.listdir(folder_path)

    for filename in tqdm(image_files, desc="Compressing images", unit="image"):
        filepath = os.path.join(folder_path, filename)
        output_filepath = os.path.join(output_path, filename)

        try:
            with Image.open(filepath) as img:
                img.save(output_filepath, optimize=True, quality=quality)
        except Exception as e:
            print(f"Failed to compress image '{filename}': {e}")


if __name__ == "__main__":
    input_folder = r"H:\Project\Java\Wechat-miniprogram-Milktea-Shop\小程序\milktea\images"
    output_folder = r"H:\Project\Java\Wechat-miniprogram-Milktea-Shop\小程序\milktea\compressed_images"

    compress_images(input_folder, output_folder, quality=80)
