# -*- coding:utf-8 -*-
"""
@Author  : dsw
@Email   : 544882167@qq.com
@Time    : 2024/11/13 上午 10:58
@File    : 2.0.py
@Software: PyCharm
@Brief   : 
"""
import asyncio
import time
import threading
import cv2
import numpy as np
import websockets

f = False
iplist = ["0.0.0.0", "[::]"]
box1 = None
box = None
is_changed = True

class Queue:
    def __init__(self):
        self.queue = []
        self.max_size = 3

    def push(self, item):
        if len(self.queue) >= self.max_size:
            self.queue.pop(0)
        self.queue.append(item)

    def pop(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None


# 新增的变化检测函数
def detect_change():
    global box1, is_changed
    difference = cv2.subtract(box, box1)  # 计算两帧之间的差异
    changes = np.sum(np.abs(difference))  # 计算差异的绝对值之和
    #print("Changes:", changes)
    if f:
        if changes > 4000:  # 如果有变化

            box1 = box  # 返回变化状态和当前框
            is_changed = True  # 置标志位

        else:

            is_changed = False  # 置标志位


async def camera_stream(websocket, path):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    global box1
    global box
    global is_changed  # 定义一个标志位，用于判断是否有变化
    box1 = box = cv2.resize(frame, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)  # 选取区
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            box = cv2.resize(frame, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)  # 选取区

            detect_change()
            if not is_changed:  # 如果有变化
                continue
            # 将帧编码为 JPEG
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])  # 使用80的质量
            # 通过 WebSocket 发送图像数据
            frame_data = buffer.tobytes()
            await websocket.send(frame_data)

    finally:
        cap.release()


async def main(ip):
    server = await websockets.serve(camera_stream, ip, 8000)
    print("WebSocket server is running on ws://{}:8000".format(ip))
    await server.wait_closed()


def run(flag):
    ip = iplist[flag]
    asyncio.run(main(ip))


if __name__ == '__main__':
    threads = []
    cs = {"y": True, "n": False}
    user_input = input("是否开启帧过滤(y/n)\n")

    if user_input in cs:
        f = cs[user_input]
    else:
        print("输入无效，程序将退出。")
        exit(1)

    for i in range(2):  # 开启两个线程
        thread = threading.Thread(target=run, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:  # 等待所有线程完成
        thread.join()
time.sleep(10)