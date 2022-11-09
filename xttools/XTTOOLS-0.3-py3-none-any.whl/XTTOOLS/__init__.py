from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from decimal import Decimal
import orjson
from typing import Any
from starlette.responses import JSONResponse
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


class XTJsonResponse(JSONResponse):
    media_type = "application/json"
    def __init__(
        self,
        content: Any,
        striplang:str='',
        **kwargs: Any
    ) -> None:
        if striplang:
            self.striplang =striplang if  striplang[0]=='_' else '_'+striplang
        else:
            self.striplang=''
        super().__init__(content, **kwargs)
    def render(self, content: Any) -> bytes:
        return toBytesJson(content,self.striplang)