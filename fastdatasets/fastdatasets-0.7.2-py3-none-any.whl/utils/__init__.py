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
        callback: data_input process startup
    '''

    def on_input_startup(self):
        ...

    '''
        callback: data_input process
    '''

    def on_input_process(self, index, x):
        return x

    '''
        callback: data_input process cleanup
    '''

    def on_input_cleanup(self):
        ...

    '''
        startup
    '''

    def on_output_startup(self):
        ...

    '''
        process
    '''

    def on_output_process(self, index, x):
        return x

    '''
        cleanup
    '''

    def on_output_cleanup(self):
        ...



def parallel_apply(data: typing.List,parallel_node: C_parallel_node):
    q_in = Manager().Queue(parallel_node.input_queue_size) if parallel_node.input_queue_size > 0 else Manager().Queue()
    q_out = Manager().Queue(parallel_node.output_queue_size) if parallel_node.output_queue_size > 0 else Manager().Queue()

    def worker_input(q_in: Queue, q_out: Queue,
                      startup_fn: typing.Callable,
                      process_fn: typing.Callable,
                      cleanup_fn: typing.Callable,
                      ):
        startup_fn()
        while True:
            index,x = q_in.get()
            if index is None:
                break
            res = process_fn(index,x)
            q_out.put((index,res))

        cleanup_fn()

    def worker_output(q_out: Queue, total: int,
                           startup_fn: typing.Callable,
                           process_fn: typing.Callable,
                           cleanup_fn: typing.Callable,
                           ):
        startup_fn()
        __n__ = 0
        while True:
            index,x = q_out.get()
            process_fn(index,x)
            __n__ += 1
            if __n__ == total:
                break
        cleanup_fn()

    total = len(data)
    pools = []
    for _ in range(parallel_node.num_process_worker):
        p = Process(target=worker_input, args= (q_in,
                                                q_out,
                                                parallel_node.on_input_startup,
                                                parallel_node.on_input_process,
                                                parallel_node.on_input_cleanup,
                                                ))
        pools.append(p)
        p.start()

    p = Process(target=worker_output, args=(q_out,
                                            total,
                                            parallel_node.on_output_startup,
                                            parallel_node.on_output_process,
                                            parallel_node.on_output_cleanup
                                            ))
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
        q_in.put((i,data[i]))

    for _ in range(parallel_node.num_process_worker):
        q_in.put((None, None))

    for p in pools:
        p.join()

