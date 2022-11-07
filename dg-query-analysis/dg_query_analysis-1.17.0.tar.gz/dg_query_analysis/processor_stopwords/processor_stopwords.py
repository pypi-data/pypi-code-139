import os
import json
from dg_query_analysis.processor_base import ProcessorBase, Output, ParaError



class ProcessorStopwords(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorStopwords, self).__init__(*args, **kwargs)
        self._rds_prefix = "%s:stop" % os.getenv("PRO_NAME", "Pangu")

    def _get_stopwords(self, dict_ids):
        dt_words_list = set()
        for dict_id in dict_ids:
            rds_key = f"{self._rds_prefix}:idx_{dict_id}"
            words = self.rds.get(rds_key)
            dt_words_list |= set(json.loads(words)) if words else set()
        return dt_words_list

    def _get_words_extended(self, **kwargs):
        params = kwargs.get('params')
        search_core = params.get('search_core')
        core_type = params.get('core_type')
        if not search_core or not core_type:
            print("empty search core or core type: %s" % params)
            return {}
        dict_id_list = self.g_rds_mapping_dao.get_stopwords_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return {}
        try:
            words_list = list(self._get_stopwords(dict_id_list))
            return words_list
        except Exception as e:
            print("get stopwords from redis error: %s" % e)
        return {}

    def run(self, **kwargs):
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        self.rds = interaction[1]
        self.g_rds_mapping_dao = interaction[2]
        # 这里需要用到config对象，做判断
        try:
            if not self.rds:
                raise ParaError("Stopwords g_rds_client类未找到, 请传入g_rds_client关键字参数")
            if not self.g_rds_mapping_dao:
                raise ParaError("Stopwords g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        stopwords = self._get_words_extended(**kwargs)

        return Output(stopwords=stopwords)




class ProcessorStopwordsV73(ProcessorStopwords):
    def __init__(self, *args, **kwargs):
        super(ProcessorStopwordsV73, self).__init__(*args, **kwargs)
        self._rds_prefix = "%s:stop" % os.getenv("PRO_NAME", "Pangu")

    def _get_stopwords(self, dict_ids):
        dt_words_list = set()
        for dict_id in dict_ids:
            rds_key = f"{self._rds_prefix}:idx_{dict_id}"
            try:
                words = self.rds.smembers(rds_key)
                dt_words_list |= words if words else set()
            except:
                words = self.rds.get(rds_key)
                dt_words_list |= set(json.loads(words)) if words else set()
        return dt_words_list
    # todo: 这里用到了redis 已经解决
