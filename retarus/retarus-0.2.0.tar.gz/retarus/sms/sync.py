import asyncio
from ._async import AsyncSmsClient
from .model import Client, SmsJob


class SyncSmsClient(Client):
    def __init__(self, uris):
        self.client = AsyncSmsClient(uris)
        self.loop = asyncio.new_event_loop()

    def send_sms(self, sms: SmsJob):
        res = self.loop.run_until_complete(self.client.send_sms(sms))
        return res

    def get_sms_jobs(self, job_id: str) -> dict:
        res = self.loop.run_until_complete(self.client.get_sms_job(job_id))
        return res

    def filter_sms_jobs(self, *args, **kwargs):
        res = self.loop.run_until_complete(self.client.filter_sms_jobs(**kwargs))
        return res

    def server_version(self):
        res = self.loop.run_until_complete(self.client.server_version())
        return res
