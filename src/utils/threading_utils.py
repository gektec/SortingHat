import threading

class ThreadManager:
    def __init__(self):
        self.threads = []

    def start_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True  # 设置为守护线程，主程序退出时自动结束
        thread.start()
        self.threads.append(thread)

    def stop_all_threads(self):
        for thread in self.threads:
            thread.join(timeout=1)  # 等待线程结束，超时时间为1秒
