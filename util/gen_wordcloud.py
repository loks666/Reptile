import numpy as np
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image  # 用于处理图像

# 读取Excel文件
file_path = r'F:\Downloads\408统考院校\211\南昌大学\南昌大学-2023年\复试成绩\信息工程学院一志愿.xls'
df = pd.read_excel(file_path)

# 获取第7列的数据
column_name = df.columns[6]  # 7列对应索引6
data = df[column_name]

# 转换为字符串并拼接
text = ' '.join(data.dropna().astype(str))

# 选择字体
font_path = "D:/Adobe/预设/店铺好评赠品/300款字体模板/【醉清风制作】小清新日系PSD字体模板/附赠：字体安装教程/配套字体692款/华康钢笔体W2-1.ttf"  # 用自己的字体文件路径替换

# 创建形状掩码
mask = np.array(Image.open("tencent.jpg"))  # 用自己的形状图像替换

# 创建词云对象
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    max_words=200,
    contour_width=3,
    contour_color='steelblue',
    font_path=font_path,  # 设置字体
    mask=mask  # 设置形状掩码
)

# 生成词云
wordcloud.generate(text)

# 可视化词云
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
