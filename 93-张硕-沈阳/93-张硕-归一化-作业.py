import numpy as np
import matplotlib.pyplot as plt
import math

#归一化，（0-1）
def Normalization1(x):
    ''' x = (x - x_min)/(x_max - x_min)'''
    return [(float(i) - min(x)) / float(max(x) - min(x)) for i in x ]

#归一化，（-1-1）
def Normalization2(x):
    ''' x = (x - x_mean) / (x_max - x_min)'''
    return [(float(i) - np.mean(x)) / float(max(x) - min(x)) for i in x ]

#标准化
def z_score(x):
    '''x = (x - μ) / σ'''
    x_mean = np.mean(x)  #求出平均值μ
    s2 = sum([(i - np.mean(x)) * (i - np.mean(x)) for i in x ]) / len(x)
    s2 = math.sqrt(s2)
    return [(i - x_mean) / s2 for i in x ]

l=[-10, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 30]

l1=[]

cs = []
#计算元素出现的个数，并添加到列表c中
for i in l:
    c = l.count(i)
    cs.append(c)

a = Normalization1(l)
n = Normalization2(l)
z = z_score(l)

#可视化
plt.plot(l, cs)
plt.plot(a, cs)
plt.plot(n, cs)
plt.plot(z, cs)
plt.show()