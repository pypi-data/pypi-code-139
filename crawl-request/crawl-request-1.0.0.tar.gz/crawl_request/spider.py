import logging
from queue import Queue, Empty
import asyncio
import threading
from typing import Generator


class RequestBase:
    __slots__ = ("method", "url", "headers", "cookies", "data", "proxy", "json", "params", "timeout",)

    def __init__(
            self,
            method,
            url,
            params=None,
            headers=None,
            cookies=None,
            data=None,
            json=None,
            timeout=10,
    ):
        self.method = method
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.json = json
        self.params = params
        self.timeout = timeout
        self.proxy = None

    @property
    def get_dict(self) -> dict:
        result = {}
        for k in self.__slots__:
            result[k] = self.__getattribute__(k)
        return result


class Request:
    __slots__ = (
        "request_info", "call_back", "meta", "retry"
    )

    def __init__(
            self,
            method,
            url,
            call_back,
            params=None,
            headers=None,
            cookies=None,
            data=None,
            json=None,
            timeout=10,
            meta=None,
            retry=3,
    ):
        self.request_info = RequestBase(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json,
            params=params,
            timeout=timeout
        )
        self.call_back = call_back
        self.meta = meta
        self.retry = retry

    @staticmethod
    def get(url, call_back=None, params=None, headers=None, cookies=None, timeout=10, meta=None, retry=3):
        return Request("GET", url, call_back=call_back, params=params, headers=headers, cookies=cookies,
                       timeout=timeout,
                       meta=meta, retry=retry)

    @staticmethod
    def post(url, call_back=None, params=None, headers=None, data=None, json=None, cookies=None, timeout=10,
             meta=None, retry=3):
        return Request("POST", url, call_back=call_back, params=params, headers=headers, cookies=cookies, data=data,
                       json=json,
                       timeout=timeout, meta=meta, retry=retry)


class Response:
    __slots__ = (
        "headers", "cookies", "read", "text", "url", "request"
    )

    def __init__(self, request: Request):
        self.request = request
        self.headers = {}
        self.cookies = {}
        self.read = None
        self.text = None
        self.url = None

    @property
    def meta(self):
        return self.request.meta


class CrawlerBase:
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

    def except_request(self, request: Request, exception: Exception):
        ...

    def except_callback(self, response: Response, exception: Exception):
        ...

    def parse(self, response: Response):
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
        response = Response(task)
        req = response.request
        error = None
        for i in range(req.retry):
            try:
                error = None
                req.request_info.proxy = self.get_proxy()
                await self.__request_send(req.request_info.get_dict, response)
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
        else:
            self.__call_back(response)

    def __call_back(self, response: Response):
        try:
            next_job = response.request.call_back(response) if response.request.call_back else self.parse(response)
            self.__parse_job(next_job)
        except Exception as error:
            self.logger.error("error callback[%s]:%s" % (str(response.request.call_back), error))
            self.except_callback(response, error)

    async def __request_send(self, kwargs, response: Response):
        async with self.session.request(**kwargs, verify_ssl=False) as req:
            kwargs["url"] = req.url
            self.logger.info("success request[%(proxy)s]<%(method)s>%(url)s" % kwargs)
            response.url = req.url
            response.headers = req.headers
            response.cookies = req.cookies
            response.read = await req.read()
            response.text = await req.text()
            req.close()

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
