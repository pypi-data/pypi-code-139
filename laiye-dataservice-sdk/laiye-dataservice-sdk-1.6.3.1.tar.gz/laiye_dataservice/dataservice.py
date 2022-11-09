import logging
import requests
import json
from .enums import AuthorizationType, HttpMethod, Language
from .errors import UnsupportedAuthorizationType

logger = logging.getLogger(__name__)


class DSResult:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_amount(self):
        return self.json_data.get("amount")

    def get_code(self):
        return self.json_data.get("code")

    def get_data(self):
        return self.json_data.get('data')

    def get_error_code(self):
        return self.json_data.get('errorCode')

    def get_message(self):
        return self.json_data.get('message')

    def get_page_size(self):
        return self.json_data.get('page_size')

    def is_successfully(self):
        return self.json_data.get('successfully', False)

    def get_json_data(self):
        return self.json_data

    def __getattr__(self, item):
        return self.json_data.get(item)


class DataService:
    def __init__(
            self,
            base_url,
            auth_type=AuthorizationType.UserCenter,
            username=None,
            password=None,
            api_key=None,
            timeout_seconds=30,
            language=Language.EN
    ):
        self.base_url = base_url
        self.auth_type = AuthorizationType.analysis(auth_type)

        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.language = Language.analysis(language)

        self.access_token = None
        self.authorization = None

        self.default_header = {"Content-Type": "application/json; charset=utf-8"}

        self.token = None

        if self.auth_type == AuthorizationType.UserCenter:
            pass
        elif self.auth_type == AuthorizationType.BuiltInUser:
            result = self.get_auth_token(username, password)
            if result.get_code() != 200 or result.get_data() is None:
                raise Exception("Get token error, please confirm your base_url, username or password")
                return
            self.token = result.get_data().get('token')
        elif self.auth_type == AuthorizationType.JwtToken:
            pass
        else:
            raise UnsupportedAuthorizationType(self.auth_type)

    def _get_authorized_header(self):
        header = self.default_header.copy()

        if self.auth_type == AuthorizationType.UserCenter:
            pass
        elif self.auth_type == AuthorizationType.BuiltInUser:
            header["Authorization"] = self.token
        elif self.auth_type == AuthorizationType.JwtToken:
            header["Jwt-Token"] = self.token
        else:
            raise UnsupportedAuthorizationType(self.auth_type)

        return header

    def _query(self, http_method, api_url, data=None, api_version='v1', if_need_auth=True):
        if if_need_auth:
            header = self._get_authorized_header()
        else:
            header = self.default_header.copy()

        header["Accept-Language"] = self.language.value

        url = f"{self.base_url}/api/{api_version}{api_url}"
        if http_method == HttpMethod.GET:
            response = requests.get(
                url,
                headers=header,
                timeout=self.timeout_seconds
            )
        elif http_method == HttpMethod.POST:
            response = requests.post(
                url,
                headers=header,
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                timeout=self.timeout_seconds
            )
        else:
            logger.error(f"unsupported request method {http_method}")
            raise Exception(f"unsupported request method {http_method}")

        return response

    @staticmethod
    def _resolve_response(
            res, if_log_error_when_not_200=True, if_resolve_json_body_when_not_200=False, url=''
    ) -> DSResult:
        if res is None:
            logger.error("Response is none")
            raise Exception("Response is none")

        if res.status_code != 200 and if_log_error_when_not_200:
            logger.error(f'Request to [{url}] failed, res status [{res.status_code}], res content [{res.text}]')

        if res.status_code == 200 or if_resolve_json_body_when_not_200:
            data = res.json()
            return DSResult(data)

        return DSResult({"code": res.status_code, "errorCode": 0, "successfully": False})

    """Auth"""
    def get_auth_token(self, username, password) -> DSResult:
        url = f'/user/auth'
        res = self._query(HttpMethod.POST, url, data={"username": username, "password": password}, if_need_auth=False)
        result = self._resolve_response(res, if_log_error_when_not_200=True, url=url)
        if result.get_code() != 200:
            logger.warning(
                f'get auth token error, message=[{result.get_message()}], status_code=[{result.get_code()}],'
                f' error_code={result.get_error_code()}'
            )
        return result

    def logout(self):
        url = f'/user/logout'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    """ Schema """
    def create_schema(self, api_name, display_name, description='') -> DSResult:
        url = f'/ddl/schema/add'
        data = {
            "apiName": api_name,
            "description": description,
            "displayName": display_name,
            "etag": 0,
            "ifEnableCls": False,
            "ifEnableRls": False
        }
        res = self._query(HttpMethod.POST, url, data=data)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_schema(self, schema_api_name, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/delete/{schema_api_name}?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_schemas(self, start_id=0, limit=1000, order='asc', expansion_level=2) -> DSResult:
        url = f'/ddl/schema/read/?startId={start_id}&limit={limit}&order={order}&expansionLevel={expansion_level}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_schema(self, schema_api_name, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/read/{schema_api_name}?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_fields(self, schema_api_name, fields, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/{schema_api_name}/field/add?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.POST, url, data=fields)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_fields(self, schema_api_name, field_api_names, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/{schema_api_name}/field/delete?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.POST, url, data=field_api_names)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_index(self, schema_api_name, index, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/{schema_api_name}/index/add?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.POST, url, data=index)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_index(self, schema_api_name, index_api_name, expansion_level=2) -> DSResult:
        url = f'/ddl/schema/{schema_api_name}/index/read/{index_api_name}?expansionLevel={expansion_level}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    """ Data """

    def add_record(self, schema_api_name, record, update_or_insert=False, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/add?upsert={update_or_insert}&responseWithData={response_with_data}'
        res = self._query(HttpMethod.POST, url, data=record)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def add_records(self, schema_api_name, records, update_or_insert=False, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/add-batch?upsert={update_or_insert}&responseWithData={response_with_data}'
        res = self._query(HttpMethod.POST, url, data=records)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_records(self, schema_api_name, record_ids, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/delete-batch?responseWithData={response_with_data}'
        res = self._query(HttpMethod.POST, url, data=record_ids)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def delete_record(self, schema_api_name, record_id, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/delete/{record_id}?responseWithData={response_with_data}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def search_records(self, schema_api_name, search_data) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/query-data'
        res = self._query(HttpMethod.POST, url, data=search_data)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def get_records(self, schema_api_name, start_id=0, limit=1000, order='asc') -> DSResult:
        url = f'/dml/entity/{schema_api_name}/read?startId={start_id}&limit={limit}&order={order}'
        res = self._query(HttpMethod.GET, url)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def update_records(self, schema_api_name, records, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/update-batch?responseWithData={response_with_data}'
        res = self._query(HttpMethod.POST, url, data=records)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def update_record(self, schema_api_name, record_id, record, response_with_data=False) -> DSResult:
        url = f'/dml/entity/{schema_api_name}/update/{record_id}?responseWithData={response_with_data}'
        res = self._query(HttpMethod.POST, url, data=record)
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)

    def exec_select_sql(self, select_sql) -> DSResult:
        url = f'/dml/sql/execute'
        res = self._query(HttpMethod.POST, url, data={"query": select_sql})
        return self._resolve_response(res, if_log_error_when_not_200=True, url=url)



