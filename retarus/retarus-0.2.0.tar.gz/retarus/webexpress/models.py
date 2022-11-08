import io
from typing import Optional
from aiohttp import FormData
from pydantic import BaseModel
import json
import os

from retarus.common.config import Configuration


class ListImport(BaseModel):
    j_username: Optional[str]  
    j_password: Optional[str]
    dlu_listname: str
    dlu_listcomment: str
    dlu_type: str = "distributionlist"
    dlu_file: str
    dlu_charset: str = "UTF-8"
    dlu_visibility: Optional[str] = "company"
    dlu_defaultcountrycode: str
    dlu_firstrowcolumnnames: str = "on"
    
    def from_file(list_comment: str, file_path: str, dlu_defaultcountrycode: str = "+49", dlu_firstrowcolumnnames: str = "on"):
        """
        Builds a request object that will be send to the server to import the customer list.
        expects a file with following columns headings: id, email, sms, fax

            list_comment: Add context for your coworkers, like "Customers who regularly order".
            file_path: where the file is stored on you machine, like "customer.csv".
            dlu_defaultcountrycode: The default country code that will be used, if you phone number does not contain a country code.
            dlu_firstrowcolumnnames: Must be 'on'

        """
        x = ListImport(dlu_listname=os.path.basename(file_path),
        dlu_listcomment=list_comment,
        dlu_defaultcountrycode=dlu_defaultcountrycode,
        dlu_type="distributionlist", dlu_file=file_path,
        dlu_firstrowcolumnnames=dlu_firstrowcolumnnames
        )
        return x


def import_to_form(data: ListImport):
    """
    Builds a form-data dictionary out of a jsonifyed ListImpor object. 
    """
    if Configuration.webexpress_auth_user_id != "":
        data.j_username = Configuration.webexpress_auth_user_id
        data.j_password = Configuration.webexpress_auth_password
    raw_data = json.loads(data.json())
    fields = {}
    for x, y in raw_data.items():
        if y is None:
            continue
        if x == "dlu_file":
            fields[x] = (raw_data["dlu_listname"], open(y, 'rb',), 'text/csv')
            continue
        fields[x] = (None, y, "text/plain")
    return fields


class Client(object):
    def upload_distributor_list(self, data: ListImport):
        """
        Takes your [ListImport] and sends it to the server, where is determine if the syntax of your submitted file is correct.
        """
        pass