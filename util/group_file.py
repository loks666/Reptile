import os
import shutil

# 指定文件夹路径
src_dir = r"F:\Downloads\百度云下载\【09】雅思\文件等多个文件\我的资源\资料23\[02]23雅思101基础班"

# 获取文件夹中的所有文件
files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]

# 创建一个字典来存储前缀和对应的文件
prefix_dict = {}

for file in files:
    # 假设前缀是文件名中的前6个字符，您可以根据需要调整
    prefix = file[:6]
    if prefix not in prefix_dict:
        prefix_dict[prefix] = []
    prefix_dict[prefix].append(file)

# 根据前缀创建文件夹并移动文件
for prefix, files in prefix_dict.items():
    new_dir = os.path.join(src_dir, prefix)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    for file in files:
        shutil.move(os.path.join(src_dir, file), os.path.join(new_dir, file))

print("Files moved successfully!")
