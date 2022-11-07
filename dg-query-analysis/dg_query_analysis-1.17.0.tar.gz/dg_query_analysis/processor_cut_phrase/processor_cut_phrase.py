import os
import json
import threading
from dg_query_analysis.processor_base import ParaError, Output
from dg_query_analysis.processor_cut_words.processor_cut_words import ProcessorCutWords, ProcessorCutWordsV70

class ProcessorCutPhrase(ProcessorCutWords):
    # todo：这里继承cutwords

    def __init__(self, *args, **kwargs):
        super(ProcessorCutPhrase, self).__init__(*args, **kwargs)
        self._rds_prefix = "%s:cut" % self._proj
        self.lock = threading.RLock()

    def _get_inverted_words(self, words, **kwargs):
        params = kwargs.get('params')
        search_core = params.get('search_core')
        core_type = params.get('core_type')
        if not search_core or not core_type:
            print("empty search core or core type: %s" % params)
            return []
        dict_id_list = self.g_rds_mapping_dao.get_phrase_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return []
        words = [w.lower().strip() for w in words]
        redis_keys = [f"{self._rds_prefix}:idx_{dt_id}:{self._md5(w_hex)[:8]}"
                      for dt_id in dict_id_list for w_hex in words]
        try:
            words_list = self.rds.mget(redis_keys)  # [json.dumps([]), ..., ]
            words = []
            for ws_str in words_list:
                ws_list = []
                if ws_str:
                    ws_list = json.loads(ws_str)
                words += ws_list
            return list(set(words))
        except Exception as e:
            print("get inverted words from redis error: %s" % e)
        return []

    @staticmethod
    def _rm_fake_words(called_words, **kwargs):
        params = kwargs.get('params')
        query = params.get('query') or None
        if not query:
            return []
        tmp_q = query.replace(" ", "").lower()
        real_words = []
        for w in called_words:
            w_lower = w.replace(" ", "").lower()
            if w_lower in tmp_q:
                real_words.append(w)
        return real_words

    @staticmethod
    def _get_longest_phrase(phrase_list):
        length = len(phrase_list)
        phrases = []
        for idx in range(length):
            is_kept = True
            for jdx in range(length):
                if idx == jdx:
                    continue
                else:
                    if phrase_list[idx] in phrase_list[jdx]:
                        is_kept = False
                        break
            if is_kept:
                phrases.append(phrase_list[idx])
        return phrases

    def get_phrase_words(self, **kwargs):
        params = kwargs.get('params')
        cut_words = params.get("cut_words") or [w.word for w in self._run_cut(**kwargs)]
        called_words = self._get_inverted_words(cut_words, **kwargs)
        phrase_words = self._rm_fake_words(called_words, **kwargs)
        return self._get_longest_phrase(phrase_words)

    def run(self, **kwargs):
        new_params = kwargs.get('query_analysis_params', {})
        self.interaction = self.get_kwargs(new_params)
        self.g_rds_mapping_dao = self.interaction[2]
        self.rds = self.interaction[1]
        # 这里需要用到g_rds_mapping_dao对象，做判断
        try:
            if not self.g_rds_mapping_dao:
                raise ParaError("cut_phrase :g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
            if not self.rds:
                raise ParaError("cut_phrase: rds类未找到, 请传入g_rds_client关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))

        phrase = self.get_phrase_words(**kwargs)
        return Output(phrase=phrase)



class ProcessorCutPhraseV70(ProcessorCutWordsV70):
    # todo：继承
    def __init__(self, *args, **kwargs):
        super(ProcessorCutPhraseV70, self).__init__(*args, **kwargs)
        self._proj = os.getenv("PROJ_NAME", "Pangu")
        self._rds_prefix = "%s:cut" % self._proj
        self.lock = threading.RLock()

    def _get_inverted_words(self, words, **kwargs):
        params = kwargs.get('params')
        search_core = params.get('search_core')
        core_type = params.get('core_type')
        if not search_core or not core_type:
            print("empty search core or core type: %s" % params)
            return []

        dict_id_list = self.g_rds_mapping_dao.get_phrase_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return []
        words = [w.lower().strip() for w in words]
        redis_keys = [f"{self._rds_prefix}:idx_{dt_id}:{self._md5(w_hex)[:8]}" # todo：这里需要md5
                      for dt_id in dict_id_list for w_hex in words]
        try:
            words_list = self.rds.mget(redis_keys)  # [json.dumps([]), ..., ] # todo：这里传redis类
            words = []
            for ws_str in words_list:
                ws_list = []
                if ws_str:
                    ws_list = json.loads(ws_str)
                words += ws_list
            return list(set(words))
        except Exception as e:
            print("get inverted words from redis error: %s" % e)
        return []

    @staticmethod
    def _rm_fake_words(called_words, **kwargs):
        params = kwargs.get('params')
        query = params.get('query') or None
        if not query:
            return []
        tmp_q = query.replace(" ", "").lower()
        real_words = []
        for w in called_words:
            w_lower = w.replace(" ", "").lower()
            if w_lower in tmp_q:
                real_words.append(w)
        return real_words

    @staticmethod
    def _get_longest_phrase(phrase_list):
        length = len(phrase_list)
        phrases = []
        for idx in range(length):
            is_kept = True
            for jdx in range(length):
                if idx == jdx:
                    continue
                else:
                    if phrase_list[idx] in phrase_list[jdx]:
                        is_kept = False
                        break
            if is_kept:
                phrases.append(phrase_list[idx])
        return phrases

    def get_phrase_words(self, **kwargs):
        params = kwargs.get('params')
        cut_words = params.get("cut_words") or [w.word for w in self._run_cut(**kwargs)]
        called_words = self._get_inverted_words(cut_words, **kwargs)
        phrase_words = self._rm_fake_words(called_words, **kwargs)
        return self._get_longest_phrase(phrase_words)

    def run(self, **kwargs):
        new_params = kwargs.get('query_analysis_params', {})
        self.interaction = self.get_kwargs(new_params)
        self.g_rds_mapping_dao = self.interaction[2]
        self.rds = self.interaction[1]
        # 这里需要用到g_rds_mapping_dao对象，做判断
        try:
            if not self.g_rds_mapping_dao:
                raise ParaError("Cut_Phrase g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
            if not self.rds:
                raise ParaError("Cut_Phrase rds类未找到, 请传入g_rds_client关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        phrase = self.get_phrase_words(**kwargs)
        return Output(phrase=phrase)

