import os
import json
from dg_query_analysis.processor_base import ProcessorBase, Output, ParaError

class ProcessorScope(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorScope, self).__init__(*args, **kwargs)
        self._rds_prefix = "%s:scope" % os.getenv("PRO_NAME", "Pangu")

    def get_scope_words(self, dt_words_list):
        redis_keys = [f"{self._rds_prefix}:idx_{dt_id}:gp:{self._md5(w)[:8]}" for dt_id, w in dt_words_list]
        words_list = self.rds.mget(redis_keys)
        result_list = {}
        words_list = [json.loads(w) if w else [] for w in words_list]
        for dt in dt_words_list:
            result_list[dt[1]] = words_list[dt_words_list.index(dt)]
        return result_list

    def _get_words_extended(self, **kwargs):
        params = kwargs.get('params')
        search_core = params.get('search_core')
        root_words = params.get('root_words')
        core_type = params.get('core_type')
        if not search_core or not core_type:
            print("empty search core or core type: %s" % params)
            return {}
        dict_id_list = g_rds_mapping_dao.get_scope_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return {}
        try:
            dt_words_list = [(dt_id, w) for dt_id in dict_id_list for w in root_words]
            words_list = self.get_scope_words(dt_words_list)
            return words_list
        except Exception as e:
            print("get inverted words from redis error: %s" % e)
        return {}

    def run(self, **kwargs):
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        self.rds = interaction[1]
        self.g_rds_mapping_dao = interaction[2]
        # 这里需要用到g_rds_client对象和g_rds_mapping_dao，做判断
        try:
            if not self.rds:
                raise ParaError("Scope g_rds_client类未找到, 请传入g_rds_client关键字参数")
            if not self.g_rds_mapping_dao:
                raise ParaError("Scope g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        scope = self._get_words_extended(**kwargs)
        return Output(scope_words=scope)
