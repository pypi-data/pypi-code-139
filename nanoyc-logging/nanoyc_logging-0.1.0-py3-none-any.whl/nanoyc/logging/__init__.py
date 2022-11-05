from yandexcloud import SDK
from yandex.cloud.logging.v1.log_ingestion_service_pb2_grpc import LogIngestionServiceStub
from yandex.cloud.logging.v1.log_ingestion_service_pb2 import WriteRequest
from yandex.cloud.logging.v1.log_entry_pb2 import IncomingLogEntry, Destination, LogLevel

from google.protobuf.timestamp_pb2 import Timestamp
import json

class CloudLogger:
    def __init__(self,log_group_id, iam_token=None, service_account_key=None,service_account_file=None):

        if any([iam_token,service_account_key,service_account_file]):
            if iam_token:
                sdk=SDK(iam_token=iam_token)
            if service_account_key:
                sdk=SDK(service_account_key=service_account_key)
            if service_account_file:
                with open(service_account_file,'r') as f:
                    service_account_key=json.loads(f.read())
                sdk=SDK(service_account_key=service_account_key)
        else:
            sdk=SDK()

        self.log_group_id=log_group_id
        self._logging_service=sdk.client(LogIngestionServiceStub)


    def _write(self,level,message,json_payload=None):
        _timestamp = Timestamp()
        _timestamp.GetCurrentTime()

        entries=[
           IncomingLogEntry(
                timestamp=_timestamp,
                message=message,
                level=level,
                json_payload=json_payload
            )
        ]
        return self._logging_service.Write(
                        WriteRequest(
                            destination=Destination(
                                log_group_id=self.log_group_id
                                ),
                            entries=entries)
                        )   


    def trace(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.TRACE,
                message=message,
                json_payload=json_payload
            )


    def debug(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.DEBUG,
                message=message,
                json_payload=json_payload
            )


    def info(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.INFO,
                message=message,
                json_payload=json_payload
            )


    def warn(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.WARN,
                message=message,
                json_payload=json_payload
            )


    def error(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.ERROR,
                message=message,
                json_payload=json_payload
            )


    def fatal(self,message:str,json_payload=None):
        return self._write(
                level=LogLevel.FATAL,
                message=message,
                json_payload=json_payload
            )        
