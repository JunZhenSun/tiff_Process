import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = "C:/Users/dell/Desktop/转股价值与转股价的拟合图.csv"
data = np.array(np.loadtxt(path, dtype=str, delimiter=',', skiprows=1, usecols=(5, 6), encoding='utf-8'))
head = np.array(np.loadtxt(path, dtype=str, delimiter=',', skiprows=1, usecols=2, encoding='utf-8'))
data = np.delete(data, [-1, -2], axis=0)
head = np.delete(head, [-1, -2], axis=0)

j = 0
# 缩短标签
for i in head:
    head[j] = i.split('转')[0]
    j = j + 1
j = 0
for k in data[:, 1]:
    data[j, 1] = k.split('*')[0]
    j = j + 1

axes = plt.gca()
datax = data[:, 0].astype(float)
datay = data[:, 1].astype(float)

xmin = datax.min()
xmax = datax.max()
ymin = datay.min()
ymax = datay.max()

# 绘制拟合曲线
parameter = np.polyfit(datax, datay, 2)
p = np.poly1d(parameter)
x = np.array(range(int(xmin), int(xmax), 1))
plt.plot(x, p(x), color='r')

plt.xlabel('转股价值')
plt.ylabel('转股价')
plt.title('股价藏宝图')

plt.scatter(datax, datay)
for i in range(len(datax)):
    plt.annotate(head[i], xy=(datax[i], datay[i]),
                 xytext=(datax[i] + 0.1, datay[i] + 0.1))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
plt.show()
plt.legend(['拟合曲线', '散点图'])
print(data[-10:-1, :])
