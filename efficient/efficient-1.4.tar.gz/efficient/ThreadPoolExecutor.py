import time
import logging
import traceback
import threading

"""
2019-09-04
本来我觉得原生的线程池应该比较好，可是我发现
from concurrent.futures import ThreadPoolExecutor, wait 
该线程池控制线程启动的时候，并不精确，我本来只想一次只运行一个
所以今天决定继续完善
"""

TH_LOCK = threading.RLock()  # 线程锁


class ThreadPoolExecutor:
    done_count = 0  # 完成数
    tasks_count = 0  # 任务数
    max_workers = 1  # 线程池最大执行数量
    running_count = 0  # 正在执行的线程数
    _all_thread_box = []  # 所有待运行的线程
    _th_running_box = []  # 正在运行的线程

    def __init__(self, max_workers=None):
        if max_workers:
            self.max_workers = max_workers
        self._all_thread_box = []
        self._th_running_box = []

    def submit(self, target, *args):
        def wrapper():
            global TH_LOCK
            try:
                target(*args)
            except Exception as e:
                logging.debug('{}'.format(e))
                traceback.print_exc()
            finally:
                TH_LOCK.acquire()
                self._th_running_box.remove(threading.current_thread())
                self.done_count += 1
                TH_LOCK.release()

        self._all_thread_box.append(threading.Thread(target=wrapper))

    def run(self):
        self.tasks_count = len(self._all_thread_box)
        while len(self._th_running_box) > 0 or len(self._all_thread_box) > 0:
            rm_th = []  # 准备运行的线程
            for th in self._all_thread_box:
                if len(self._th_running_box) >= self.max_workers:
                    break
                self._th_running_box.append(th)
                th.start()
                rm_th.append(th)
            # 删除已经运行了的线程
            for rm in rm_th:
                self._all_thread_box.remove(rm)
            self.running_count = len(self._th_running_box)
            time.sleep(0.001)

    def __del__(self):
        logging.debug('所有线程结束')
        print('所有线程结束')


if '__main__' == __name__:
    def f(_id):
        print(_id)
        time.sleep(2)


    exe = ThreadPoolExecutor(max_workers=5)
    for i in range(10):
        exe.submit(f, i)
    exe.run()
