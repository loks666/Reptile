import os
import time
from pathlib import Path

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, MofNCompleteColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table

print()
path = Path(r"D:\Users\Documents\预设\格式化文件")
# 获取文件夹下的所有文件
file_list = list(path.glob("**/*"))
total = len(file_list)

job_progress = Progress(
    "{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    auto_refresh=False,
)

overall_progress = Progress(
    "{task.description}",
    BarColumn(),
    MofNCompleteColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    auto_refresh=False,
)
overall_task = overall_progress.add_task("总进度", total=total)

progress_table = Table.grid()
progress_table.add_row(Panel.fit(overall_progress, title="总进度", border_style="green"))
progress_table.add_row(Panel.fit(job_progress, title="[b]子进度", border_style="red"))


def get_direct_sub_folders(father_path):
    sub_folders = [f for f in os.listdir(father_path) if os.path.isdir(os.path.join(father_path, f))]
    return sub_folders


# 使用 Live 类开始实时渲染进度条
with Live(progress_table, refresh_per_second=10):
    # 获取路径的子文件夹名称列表
    sub_folder_list = get_direct_sub_folders(path)
    # 创建子文件夹名称的任务列表
    for sub_folder_name in sub_folder_list:
        total = len(list(path.glob(f"{sub_folder_name}/**/*")))
        job_progress.add_task(f"{sub_folder_name}", total=total)
    # 遍历文件夹下的所有文件
    for file in file_list:
        # 处理文件的原始代码已被注释掉
        overall_progress.advance(overall_task)
        time.sleep(0.01)
        print(file)
        overall_progress.refresh()
        # 遍历任务列表中的每个任务
        for job in job_progress.tasks:
            # 获取任务的描述（子文件夹名称）
            sub_folder_name = job.description
            # 如果当前文件的路径包含子文件夹名称
            if sub_folder_name in str(file):
                # 推进当前任务
                job_progress.advance(job.id)
                break
