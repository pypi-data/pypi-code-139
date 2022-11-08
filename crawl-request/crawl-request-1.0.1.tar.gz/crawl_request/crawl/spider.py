import logging
from queue import Queue, Empty
import asyncio
import threading
from typing import Generator

from crawl_request.crawl.task import Request, Response

__all__ = ["BaseCrawler", "Request", "Response"]


class BaseCrawler:
    CRAWL_NAME = "CrawlerBase"
    CONCURRENCY = 64
    logger = logging

    def __init__(self):
        self.queue = Queue()
        self.loop = asyncio.new_event_loop()
        self.sem = asyncio.Semaphore(self.CONCURRENCY, loop=self.loop)
        self.forever = False

    def start_request(self):
        raise Exception("not start_request")

    def get_proxy(self):
        raise Exception("not get_proxy")

    def except_request(self, request, exception: Exception):
        ...

    def except_callback(self, response, exception: Exception):
        ...

    def parse(self, response):
        ...

    def run_daemon(self):
        # self.logger.info("start run_daemon")
        self.forever = True
        th = threading.Thread(target=self.__start_running, daemon=True)
        th.start()

    def run_forever(self):
        self.logger.info("start run_forever")
        self.forever = True
        self.__start_running()

    def run(self):
        self.logger.info("start run start_request")
        self.__start_running()

    def __parse_job(self, job):
        if isinstance(job, Generator) or isinstance(job, list):
            for req in job:
                assert isinstance(req, Request)
                self.queue.put(req)
        elif isinstance(job, Request):
            self.queue.put(job)

    def __start_running(self):
        request = self.start_request()
        self.__parse_job(request)
        self.loop.run_until_complete(self.__start())

    @staticmethod
    def post(url, call_back=None, params=None, headers=None, data=None, json=None, cookies=None, timeout=10, meta=None,
             retry=3) -> Request:
        request = Request.post(url, call_back=call_back, params=params, headers=headers, cookies=cookies, data=data,
                               json=json,
                               timeout=timeout, meta=meta, retry=retry)
        return request

    @staticmethod
    def get(url, call_back=None, params=None, headers=None, cookies=None, timeout=10, meta=None, retry=3) -> Request:
        request = Request.get(url, call_back=call_back, params=params, headers=headers, cookies=cookies,
                              timeout=timeout,
                              meta=meta, retry=retry)
        return request

    async def __start(self):
        from aiohttp import ClientSession
        while True if self.forever else not self.queue.empty():
            for task_list in self.__get_task():
                job_list = [self.__sem_request(task) for task in task_list]
                for i in range(3):
                    try:
                        async with ClientSession() as session:
                            self.session = session
                            await asyncio.wait(job_list)
                            break
                    except Exception as e:
                        self.logger.warning("retry ClientSession: %s" % str(e))

    async def __sem_request(self, task):
        async with self.sem:
            await self.__request(task)

    async def __request(self, task):
        assert isinstance(task, Request)

        req = task
        error = None
        for i in range(req.retry):
            try:
                error = None
                req.request_info.proxy = self.get_proxy()
                response = await self.__request_send(req.request_info.get_dict)
                response.meta = task.meta
                self.__call_back(task.call_back, response)
                break
            except Exception as e:
                error = e
                e_dict = req.request_info.get_dict
                e_dict['error'] = error
                self.logger.warning("retry request(%(error)s)[proxy:%(proxy)s]<%(method)s>%(url)s" % e_dict)
                self.except_request(req, error)
        if error:
            e_dict = req.request_info.get_dict
            e_dict['error'] = error
            self.logger.error(
                "error request(%(error)s)[proxy:%(proxy)s]<%(method)s>%(url)s" % e_dict)
        # else:
        #     self.__call_back(response)

    def __call_back(self, call_back_func, response: Response):
        try:
            next_job = call_back_func(response) if call_back_func else self.parse(response)
            self.__parse_job(next_job)
        except Exception as error:
            self.logger.error("error callback[%s]:%s" % (str(call_back_func), error))
            self.except_callback(response, error)

    async def __request_send(self, kwargs):
        response = Response()
        async with self.session.request(**kwargs, verify_ssl=False) as req:
            kwargs["url"] = req.url
            self.logger.info("success request[%(proxy)s]<%(method)s>%(url)s" % kwargs)
            await response.start_await(req)
            req.close()
        return response

    def __get_task(self):
        result = []
        get_func = self.queue.get_nowait
        state = True
        while state:
            try:
                data = get_func()
                assert isinstance(data, Request)
                result.append(data)
                get_func = self.queue.get_nowait
            except Empty:
                state = self.forever
                get_func = self.queue.get
                yield result
                result.clear()
