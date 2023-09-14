import os
import subprocess

# 指定ffmpeg路径
FFMPEG_PATH = "D:/mysoftware/ffmpeg/bin"


def get_video_properties(file_path):
    try:
        # 使用 ffprobe 命令行工具获取视频属性
        command = [os.path.join(FFMPEG_PATH, 'ffprobe.exe'), '-v', 'error', '-show_entries',
                   'format=duration:stream=width,height,codec_name,bit_rate', '-of', 'default=nw=1:nk=1', file_path]

        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, shell=True)
        properties = output.strip().split('\n')
        return properties
    except subprocess.CalledProcessError as e:
        print(f"Error getting properties for {file_path}: {e}")
        return None


def main():
    folder_path = "E:/group/MP4"  # 替换为您的文件夹路径
    video_files = [f for f in os.listdir(folder_path) if
                   f.lower().endswith(('.mov', '.mp4', '.m4a', '.3gp', '.3g2', '.mj2'))]

    for video_file in video_files:
        file_path = os.path.join(folder_path, video_file)
        properties = get_video_properties(file_path)
        if properties:
            print(f"Video Properties for {video_file}:")
            for prop in properties:
                print(prop)
            print("=" * 40)


if __name__ == "__main__":
    main()
