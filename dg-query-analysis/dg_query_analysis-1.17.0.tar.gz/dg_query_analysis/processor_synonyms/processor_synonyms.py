import os
import json
from dg_query_analysis.processor_base import ProcessorBase, Output, ParaError



class ProcessorSynonyms(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorSynonyms, self).__init__(*args, **kwargs)
        self._rds_prefix = "%s:synonyms" % os.getenv("PRO_NAME", "Pangu")

    @staticmethod
    def _get_root_words(**kwargs):
        params = kwargs.get('params')
        if not params.get("cut_words"):
            print("cut words should be executed before extend synonyms!!!")

        cut_words = params.get('cut_words', [])
        phrase = params.get('phrase', [])
        root_words = []
        for w in cut_words:
            flag = True
            for p in phrase:
                if w in p:
                    flag = False
                    break
            if flag:
                root_words.append(w)
        root_words += phrase
        return list(set(root_words))

    @staticmethod
    def _filter_dt_words(dt_words_list, filter_list):
        dt_len = len(dt_words_list)
        filter_len = len(filter_list)
        assert dt_len == filter_len
        filter_dt = [dt_words_list[idx] for idx in range(dt_len) if filter_list[idx]]
        filters = [filter_list[idx] for idx in range(filter_len) if filter_list[idx]]
        return filter_dt, filters

    def _get_synonyms_group_ids(self, dt_words_list):
        # todo：这里需要用到redis
        redis_keys = [f"{self._rds_prefix}:idx_{dt_id}:wd:{self._md5(w)[:8]}" for dt_id, w in dt_words_list]
        words_group_ids = self.rds.mget(redis_keys)  # [1, ..., n]
        dt_words_list, words_group_ids = self._filter_dt_words(dt_words_list, words_group_ids)
        return dt_words_list, words_group_ids

    def _get_synonyms_groups(self, dt_words_list, words_group_ids):
        group_keys = [f"{self._rds_prefix}:idx_{dt_word[0]}:gp:{self._md5(group_id)[:8]}" for dt_word, group_id in
                      zip(dt_words_list, words_group_ids)]
        synonyms_group = self.rds.mget(group_keys)
        dt_words_list, synonyms_group = self._filter_dt_words(dt_words_list, synonyms_group)
        return dt_words_list, synonyms_group

    @staticmethod
    def _merge_same_synonyms(words_dict):
        new_dict = {}
        keys = [k for k in words_dict.keys()]
        k_size = len(keys)
        for idx in range(k_size):
            flag = True
            for jdx in range(idx+1, k_size):

                size = len(words_dict[keys[idx]])
                m_size = len(words_dict[keys[idx]] | words_dict[keys[jdx]])
                i_size = len(words_dict[keys[idx]] & words_dict[keys[jdx]])
                if m_size == size and i_size == size:
                    flag = False
                    break
            if flag:
                new_dict[keys[idx]] = words_dict[keys[idx]]
        return new_dict

    def _get_synonyms_dict(self, dt_words_list, synonyms_group):
        words_dict = {}
        for dt_word, ws_str in zip(dt_words_list, synonyms_group):
            ws_list = []
            word = dt_word[1]
            if ws_str:
                ws_list = json.loads(ws_str)
            if word not in words_dict:
                words_dict[word] = set()
            sub_words = set(ws_list)
            sub_words.remove(word)
            words_dict[word] |= sub_words
        words_dict = self._merge_same_synonyms(words_dict)
        return {k: list(words_dict[k]) for k in words_dict}

    def _get_words_extended(self, words, **kwargs):
        # dict_id_list = kwargs.get('synonyms_dicts') or []  # synonyms dictionary ids
        params = kwargs.get('params')
        search_core = params.get('search_core')
        core_type = params.get('core_type')
        if not search_core or not core_type:
            print("empty search core or core type: %s" % params)
            return {}
        dict_id_list = self.g_rds_mapping_dao.get_synonyms_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return {}
        try:
            dt_words_list = [(dt_id, w) for dt_id in dict_id_list for w in words]

            dt_words_list, words_group_ids = self._get_synonyms_group_ids(dt_words_list)
            dt_words_list, synonyms_group = self._get_synonyms_groups(dt_words_list, words_group_ids)
            words_dict = self._get_synonyms_dict(dt_words_list, synonyms_group)

            return words_dict
        except Exception as e:
            print("get inverted words from redis error: %s" % e)
        return {}

    def run(self, **kwargs):
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        self.g_rds_mapping_dao = interaction[2]
        self.rds = interaction[1]
        # 这里需要用到g_rds_mapping_dao对象，做判断
        try:
            if not self.g_rds_mapping_dao:
                raise ParaError("Synonyms g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
            if not self.rds:
                raise ParaError("Synonyms g_rds_client类未找到, 请传入g_rds_client关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        root_words = self._get_root_words(**kwargs)
        synonyms = self._get_words_extended(root_words, **kwargs)
        return Output(root_words=root_words, synonyms=synonyms)

