import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from tqdm import tqdm

plt.style.use("seaborn-pastel")

font_path = r"C:\Users\lenovo\AppData\Local\Microsoft\Windows\Fonts\Alibaba-PuHuiTi-Regular.ttf"
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
print(prop.get_name())  # 显示当前使用字体的名称

font_manager.rcParams['font.family'] = 'sans-serif'  # 使用字体中的无衬线体
font_manager.rcParams['font.sans-serif'] = prop.get_name()  # 根据名称设置字体
font_manager.rcParams['font.size'] = 20  # 设置字体大小
font_manager.rcParams['axes.unicode_minus'] = False  # 使坐标轴刻度标签正常显示正负号


data = pd.read_excel(r'./all_data.xlsx', sheet_name='all_data')
data.fillna(0, inplace=True)

# # 数据信息
type_data = data.groupby('type').count()['url']
type_data = type_data.sort_values(ascending=False)

plt.figure(figsize=(10, 6))
x = np.arange(len(type_data))
plt.bar(x, type_data)
for i, j in zip(x, type_data.values):
    plt.text(i, j+0.1, j, ha='center')
plt.xticks(x, type_data.index, rotation=90)
plt.ylabel('次数')
plt.savefig('01_类别.svg')

yanqi_data = data.groupby('postpone').count()['url']
plt.pie(yanqi_data, labels=yanqi_data.index, autopct="%.2f%%")
plt.legend()
plt.savefig('01_是否延期.svg')

# # 开始分析
# ## 官网
guanwang = data.groupby('官网').count()['url']

plt.figure(figsize=(5, 5))
plt.pie(guanwang, labels=['未搭建官网', '搭建官网'], autopct="%.2f%%")
plt.legend(loc=0)
plt.savefig('02_01_官网.svg')

# ## SEO
data_SEO = data.copy()
data_SEO = data[data_SEO['官网'] == 1]
for row in range(data_SEO.shape[0]):
    if data_SEO.loc[row, 'name'] == '中国进出口商品交易会':
        data_SEO.loc[row, '预计来路'] = 0
        data_SEO.loc[row, '百度权重'] = 0

plt.figure(figsize=(5, 4))
plt.boxplot(data_SEO.sort_values('预计来路', ascending=False)['预计来路'][1:], patch_artist=True)
plt.ylabel('IP数量')
plt.xticks([1], ['预计来路'])
plt.savefig('02_02_预计来路.svg')

baiduw = data_SEO.groupby('百度权重').count()['url']
x = np.arange(len(baiduw))
plt.figure(figsize=(5, 4))
plt.bar(x,baiduw)
plt.xticks(x, [str(i) + '分' for i in baiduw.index])
for i, j in zip(x, baiduw.values):
    plt.text(i, j+2, j, ha='center')
plt.ylim(0, 125)
plt.ylabel('数量')
plt.savefig('02_02_百度权重.svg')

# ## 新闻媒体
plt.boxplot(data.loc[:,['腾讯网','新浪新闻', '搜狐新闻', '澎湃新闻', 'B站']],patch_artist=True)
plt.xticks(np.arange(1, 6),['腾讯网','新浪新闻', '搜狐新闻', '澎湃新闻', 'B站'])
plt.ylabel('报道数量')
plt.savefig('02_03_社交媒体+B站.svg')

# ## 熵权法
data_arrary = data.loc[:, ['官网', '预计来路', '百度权重', '腾讯网', '新浪新闻', '搜狐新闻', 'B站']].to_numpy()

a = data_arrary.copy()  # 深拷贝数据矩阵，便于接下来的归一化
for j in range(data_arrary.shape[1]):
    a[:, j] = a[:, j] / max(a[:, j])  # 比例变换

a = a + np.finfo(np.float32).eps  # 加一个极小的数 防止0为底数报错
[n, m] = a.shape  # 取矩阵大小
cs = a.sum(axis=0)  # 逐列求和
P = 1 / cs * a  # 求特征比重矩阵
e = -(P * np.log(P)).sum(axis=0) / np.log(n)  # 计算熵值
g = 1 - e  # 计算差异系数
w = g / sum(g)  # 计算权重
F = P @ w  # 计算各对象的评价值
print("\nP={}\n,e={}\n,g={}\n,w={}\nF={}".format(P, e, g, w, F))

data['评价值'] = F  # 保存评价值到表格
data.sort_values('评价值', ascending=False, inplace=True)  # 评价值排序
data['排名'] = np.arange(data.shape[0]) + 1  # 排名值
data.sort_index(inplace=True)  # 还原之前的顺序

data_draw = data.sort_values('评价值', ascending=False).iloc[:20, :]  # 提取画图的数据
x = np.arange(data_draw.shape[0])  # x 轴值
plt.figure(figsize=(6, 3.5))
plt.bar(x, data_draw['评价值'])  # 画图
plt.xticks(x, data_draw['index'], rotation='45')  # x轴刻度名
for i, j in zip(x, data_draw['评价值']):
    plt.text(i, j+0.003, '%.2f' % j, ha='center', size=7)
plt.ylim(0, 0.3)
plt.xlabel('展会ID')  # 横坐标标题
plt.ylabel('评价值')  # 纵坐标标题
plt.savefig('02_04_熵权法.svg')  # 保存

data.to_excel('result.xlsx')
