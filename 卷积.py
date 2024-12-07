# -*- coding:utf-8 -*-
"""
@Author  : dsw
@Email   : 544882167@qq.com
@Time    : 2024/11/13 下午 12:34
@File    : 卷积.py
@Software: PyCharm
@Brief   : 
"""
import asyncio
import time
import threading
import cv2
import numpy as np
import websockets

import matplotlib.pyplot as plt
import numpy as np
import pylab


def General_Conv(imatx, imaty, kernel, padding, photo):
    k_array = np.random.rand(kernel, kernel)  # 卷积核矩阵
    i_array = photo  # 随机数矩阵
    gap = kernel // 2  # 计数空缺的行数和列数
    new_array = np.zeros(shape=(imatx, imaty))  # 在原来的随机数矩阵外围补零
    if padding == 0:  # 不填充
        b_array = np.zeros(shape=(imatx - gap * 2, imaty - gap * 2))  # 定义一个矩阵存放卷积以后的值
        for i in range(gap, imatx - gap):
            for j in range(gap, imaty - gap):
                m_array = i_array[i - gap:i + gap + 1, j - gap:j + gap + 1]
                b_array[i - gap][j - gap] = int(np.sum(k_array * m_array))
        for x in range(imatx - 2 * gap):
            for y in range(imaty - 2 * gap):
                new_array[x + gap][y + gap] = b_array[x][y]  # 将原来的随机数矩阵填入
        return new_array
    if padding == 1:  # 填充0
        b_array = np.zeros(shape=(imatx + gap * 2, imaty + gap * 2))  # 在原来的随机数矩阵外围补零
        for i in range(imatx):
            for j in range(imaty):
                b_array[i + gap][j + gap] = i_array[i][j]  # 将原来的随机数矩阵填入
        for i in range(gap, imatx + 1):
            for j in range(gap, imaty + 1):  # gap下标实际上是第gap+1个元素的位置
                m_array = b_array[i - gap:i + gap + 1, j - gap:j + gap + 1]
                new_array[i - gap - 1][j - gap - 1] = int(np.sum(k_array * m_array))  # 为什么-1
        return new_array


# img_new = np.uint8(General_Conv(400, 300, 3, 1))
# print(img_new)
# plt.imshow(img_new)  # 卷积结果可视化
# pylab.show()
# print('*' * 40)
# img_new = np.uint8(General_Conv(10, 10, 3, 0))
# print(img_new)
# plt.imshow(img_new)  # 卷积结果可视化
# pylab.show()
cap = cv2.VideoCapture(0)
ret, src = cap.read()
print(src.shape)
dst = cv2.resize(src, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
print(dst.shape)
plt.imshow(dst)
pylab.show()
