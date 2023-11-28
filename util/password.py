from PIL import Image
import os


def rotate_images_in_directory(directory_path):
    # 获取指定路径下所有 jpg 文件
    jpg_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.jpg')]

    for jpg_file in jpg_files:
        file_path = os.path.join(directory_path, jpg_file)

        # 打开图片
        image = Image.open(file_path)

        # 逆时针旋转 90 度
        rotated_image = image.rotate(90, expand=True)

        # 保存覆盖原文件
        rotated_image.save(file_path)
        print(f"{jpg_file} 逆时针旋转完成")


if __name__ == "__main__":
    # 指定图片所在路径
    image_directory = r"F:\Downloads\local_send\旋转"

    # 调用函数旋转图片
    rotate_images_in_directory(image_directory)
