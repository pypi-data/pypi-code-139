from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from decimal import Decimal
from typing import Any
import orjson
def obj2dict(obj:Any,striplang='')->Any:#type: ignore
    if isinstance(obj,DeclarativeMeta):
        return obj.dict(striplang=striplang)
    elif isinstance(obj,BaseModel):
        return obj.dict()
    elif isinstance(obj,Decimal):
        return str(obj)
    raise Exception("object are not jsonable")

def toBytesJson(obj:Any,striplang:str='')->bytes:
    return orjson.dumps(obj,default=lambda obj :obj2dict(obj,striplang=striplang))

def toJson(obj:Any,striplang:str='')->str:
    return orjson.dumps(obj,default=lambda obj :obj2dict(obj,striplang=striplang)).decode()