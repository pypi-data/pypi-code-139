# @Time    : 2022/11/5 19:34
# @Author  : tk
# @FileName: __init__.py.py
import random
import typing
from multiprocessing import Queue,Manager,Process

__all__ = [
    'parallel_apply',
    'C_parallel_node'
]




class C_parallel_node:
    def __init__(self,  num_process_worker: int = 4,
                 num_process_post_worker: int = 1,
                 input_queue_size: int = 1000,
                 output_queue_size : int = 1000,
                 shuffle = True,
                 desc: str='parallel'):
        self.num_process_worker = num_process_worker
        self.num_process_post_worker = num_process_post_worker
        self.input_queue_size = input_queue_size
        self.output_queue_size = output_queue_size
        self.shuffle = shuffle
        self.desc = desc

        if self.input_queue_size is None:
            self.input_queue_size = -1

        if self.output_queue_size is None:
            self.output_queue_size = -1

        if self.desc is None:
            self.desc = ''

        assert num_process_worker > 0 and num_process_post_worker > 0

    '''
        callback: mutiprocess read data 
    '''
    def on_coming(self,x):
        return x

    '''
        callback:process data from on_coming 
    '''
    def on_output(self,x):
        ...

    '''
        callback:completed
    '''
    def on_done(self):
        ...


def parallel_apply(data: typing.List,parallel_node: C_parallel_node):
    q_in = Manager().Queue(parallel_node.input_queue_size) if parallel_node.input_queue_size > 0 else Manager().Queue()
    q_out = Manager().Queue(parallel_node.output_queue_size) if parallel_node.output_queue_size > 0 else Manager().Queue()

    def worker_coming(q_in: Queue, q_out: Queue, process_fn: typing.Callable):
        while True:
            x,is_end = q_in.get()
            if is_end:
                break
            res = process_fn(x)
            q_out.put(res)

    def worker_out(q_out: Queue, total: int, process_post_fn: typing.Callable):
        n = 0
        while True:
            x = q_out.get()
            process_post_fn(x)
            n += 1
            if n == total:
                break

    total = len(data)
    pools = []
    for _ in range(parallel_node.num_process_worker):
        p = Process(target=worker_coming, args=(q_in, q_out, parallel_node.on_coming))
        pools.append(p)
        p.start()

    p = Process(target=worker_out, args=(q_out, total, parallel_node.on_output))
    pools.append(p)
    p.start()

    ids = list(range(total))
    if parallel_node.shuffle:
        random.shuffle(ids)
    try:
        from tqdm import tqdm
        ids = tqdm(ids,total=total,desc=parallel_node.desc if parallel_node.desc else 'parallel_apply')
    except:
        ...
    for i in ids:
        q_in.put((data[i], False))

    for _ in range(parallel_node.num_process_worker):
        q_in.put((None, True))

    for p in pools:
        p.join()

    parallel_node.on_done()
