import ydb
import ydb.iam
import ydb.table
import os

from uuid import uuid4

class QueryResult:
    def __init__(self, ydb_result):
        self._ydb_result=ydb_result
    def get_single_value(self,parameter_name=None):
        if parameter_name:
            return self._ydb_result[0].rows[0][parameter_name]
        else:
            return next(self._ydb_result[0].rows[0].values) #return fist item in dict
    def get_single_object(self):
        return self._ydb_result[0].rows[0]
    def get_list(self):
        return self._ydb_result[0].rows

def generate_id():
    return uuid4().hex

class Ydb:
    def __init__(self,
        ydb_endpoint:str=None,
        ydb_database:str=None,
        service_account_file=None,
        iam_token=None

    ):
        #defining endpoint
        if ydb_endpoint:
            self.ydb_endpoint=ydb_endpoint
        else:
            self.ydb_endpoint=os.getenv("YDB_ENDPOINT",None)

        if not self.ydb_endpoint:
            raise Exception('nanoydb - Cant find endpoint. Specify ydb_endpoint parameter or YDB_ENDPOINT enviromental variable')
        
        #defining database
        if ydb_database:
            self.ydb_database=ydb_endpoint
        else:
            self.ydb_database=os.getenv("YDB_DATABASE",None)

        if not self.ydb_database:
            raise Exception('nanoydb - Cant find endpoint. Specify ydb_endpoint parameter or YDB_ENDPOINT enviromental variable')
        
        #Authorization

        service_account_env_file=os.getenv('SA_FILE',None)

        if iam_token:
            credentials=ydb.AccessTokenCredentials(iam_token)
        elif service_account_file:
            credentials=ydb.iam.ServiceAccountCredentials().from_file(service_account_file)
        elif service_account_env_file:
            credentials=ydb.iam.ServiceAccountCredentials().from_file(service_account_env_file)
        else:
            credentials=ydb.iam.MetadataUrlCredentials()

        self.credentials=credentials

    def do_query(self,query, timeout=2,operation_timeout=4,**params,):
        """call 
        query='SELECT ...'

        #preparing callee
        params=video_id=1, data=3 ..."""

        def callee(session:ydb.table.Session):
            nonlocal query,params
            prepared_query=session.prepare(query=query)
            prepared_params={f'${key}':params[key] for key in params}
            
            return session.transaction(ydb.SerializableReadWrite()).execute(
                query=prepared_query,
                parameters=prepared_params,
                settings=ydb.BaseRequestSettings().with_timeout(timeout).with_operation_timeout(operation_timeout),
                commit_tx=True
            )

        

        driver = ydb.Driver(
            endpoint=self.ydb_endpoint,
            database=self.ydb_database,
            credentials=self.credentials,
        )
        with driver:
            driver.wait(timeout=5,fail_fast=True)

            #making a call
            with ydb.SessionPool(driver) as pool:
                result=pool.retry_operation_sync(
                    callee
                )

            
        return QueryResult(result)