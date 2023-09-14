import os
import shutil
from tqdm import tqdm
import threading
import subprocess

def move_with_rename(src, dest):
    """将文件从src移动到dest，如果dest已存在则进行重命名。"""
    base, ext = os.path.splitext(dest)
    counter = 1
    while os.path.exists(dest):
        dest = f"{base}_{counter}{ext}"
        counter += 1
    shutil.move(src, dest)

def has_audio(file_path):
    """检查视频文件是否有声音。"""
    try:
        # 使用FFmpeg来检查视频文件是否有音频流
        command = ['ffmpeg', '-i', file_path]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        if 'Stream #0:1' in output:
            return True
    except subprocess.CalledProcessError as e:
        if "partial file" in e.output:
            print(f"File {file_path} is partial and might be corrupt.")
        else:
            print(f"Error checking file {file_path}: {e}")
    return False

def process_files(files, total_files, dest_folder, lock, thread_name):
    pbar = tqdm(total=len(files), position=thread_name, desc=f"Thread-{thread_name}", leave=True)
    for file in files:
        file_path = os.path.join(src_folder, file)
        if has_audio(file_path):
            dest_path = os.path.join(dest_folder, file)
            move_with_rename(file_path, dest_path)
        pbar.update(1)
    pbar.close()

def main():
    global src_folder
    src_folder = "E:/group/MP4/test"
    dest_folder = "E:/group/MP4/not_with_audio"
    os.makedirs(dest_folder, exist_ok=True)

    files = sorted([f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))])
    num_threads = 4  # 设定线程数，可以根据您的需要进行调整
    chunk_size = len(files) // num_threads
    threads = []
    lock = threading.Lock()  # 用于同步进度输出

    for i in range(num_threads):
        if i == num_threads - 1:
            chunk = files[i*chunk_size:]
        else:
            chunk = files[i*chunk_size:(i+1)*chunk_size]
        thread = threading.Thread(target=process_files, args=(chunk, len(files), dest_folder, lock, i))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
