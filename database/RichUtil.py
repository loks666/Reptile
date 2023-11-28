# rich_util.py
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, MofNCompleteColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table


class RichUtil:

    def __init__(self, total):
        overall_progress = Progress(
            "{task.description}",
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            auto_refresh=False,
        )
        progress_table = Table.grid()
        progress_table.add_row(Panel.fit(overall_progress, title="总进度", border_style="green"))
        self.overall_task = overall_progress.add_task("处理进度：", total=total)
        self.total_tasks = total
        self.progress_table = progress_table
        self.overall_progress = overall_progress

    def init_progress(self):
        self.overall_progress = self.create_progress_bar("总进度")

    def create_progress_bar(self, title):
        progress = Progress(
            "{task.description}",
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            auto_refresh=False,
        )
        task = progress.add_task(title, total=self.total_tasks)
        progress_table = Table.grid()
        progress_table.add_row(Panel.fit(progress, title=title, border_style="green"))
        with Live(progress_table, refresh_per_second=10):
            progress.update(task, completed=0)
        return progress

    def update_progress(self):
        self.overall_progress.advance(self.overall_task)

    def close_progress(self):
        self.overall_progress.stop()
