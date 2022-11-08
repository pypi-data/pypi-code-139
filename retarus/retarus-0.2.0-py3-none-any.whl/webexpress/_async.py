from .models import Client, ListImport, import_to_form
from ..common.transport import Transporter


class AsyncWebExpressClient(Client):
    def __init__(self, uris):
        self.__transporter = Transporter(uris)

    async def upload_distributor_list(self, data: ListImport) -> str:
        """
        Takes your [ListImport] and sends it to the server, where is determine if the syntax of your submitted file is correct.
        """
        payload = import_to_form(data)
        res = await self.__transporter.form_post(payload)
        return res