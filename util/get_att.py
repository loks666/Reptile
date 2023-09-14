import os
import shutil
from pymediainfo import MediaInfo


def move_file(src, dest_folder):
    """移动文件到目标目录，确保文件名不重复"""
    base, ext = os.path.splitext(os.path.basename(src))
    dest = os.path.join(dest_folder, f"{base}{ext}")
    counter = 1

    while os.path.exists(dest):  # 检查文件是否重名
        dest = os.path.join(dest_folder, f"{base}_{counter}{ext}")
        counter += 1

    shutil.move(src, dest)


def process_video_files(root_dir):
    """处理指定目录下的视频文件"""
    for root, _, files in os.walk(root_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            media_info = MediaInfo.parse(file_path)

            video_track = next((track for track in media_info.tracks if track.track_type == "Video"), None)

            if video_track:
                width = getattr(video_track, 'width', None)
                height = getattr(video_track, 'height', None)

                if width is None or height is None:
                    print(f"文件名: {filename}\t宽度或高度缺失\t路径: {file_path}")
                    continue

                if width >= 1920 and height >= 1080:
                    ensure_directory_exists("E:/group/mov/high/")
                    move_file(file_path, "E:/group/mov/high/")
            else:
                print(f"文件名: {filename}\t未找到视频轨道\t路径: {file_path}")
                ensure_directory_exists("E:/group/mov/no_video/")
                move_file(file_path, "E:/group/mov/no_video/")


def ensure_directory_exists(directory):
    """确保指定的目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    process_video_files("E:/group/mov/")
    print("视频处理完成")
