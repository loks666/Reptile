import pandas as pd

if __name__ == '__main__':
    # 使matplotlib模块能显示中文
    mpl.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    # 1、读取数据
    df = pd.read_csv('./JobPosition/Python开发.csv', encoding='utf-8')
