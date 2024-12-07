import asyncio
import time
import threading
import cv2
import numpy as np
import websockets

f = False
iplist = ["0.0.0.0", "[::]"]


class queue:
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


async def camera_stream(websocket, path):
    cap = cv2.VideoCapture(0)
    box1 = np.zeros((200, 200, 3), np.uint8)  # 定义一个空白的图像
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            box = frame[100:300, 100:300]  # 选取区
            difference = cv2.subtract(box, box1)  # 计算两帧之间的差异
            if f:
                if sum(difference[difference > 0]) > 40000:  # 如果两帧之间的差异大于 0，说明有变化
                    box1 = box
                    # print("change detected")
                else:
                    # print("no change")
                    continue
            # 将帧编码为 JPEG
            _, buffer = cv2.imencode('.jpg', frame)  #
            # 通过 WebSocket 发送图像数据
            frame_data = buffer.tobytes()
            await websocket.send(frame_data)

    finally:
        cap.release()


async def main(ip):
    server = await websockets.serve(camera_stream, ip, 8000)  #
    print("WebSocket server is running on ws://{}:8000".format(ip))
    await server.wait_closed()


def run(flag):
    ip = iplist[flag]

    asyncio.run(main(ip))


if __name__ == '__main__':
    threads = []
    cs = {"y": True, "n": False}
    f = cs[input("是否开启帧过滤(y/n)\n")]
    for i in range(2):  # 开启两个线程
        thread = threading.Thread(target=run, args=(i,))
        threads.append(thread)
        thread.start()
time.sleep(10)
