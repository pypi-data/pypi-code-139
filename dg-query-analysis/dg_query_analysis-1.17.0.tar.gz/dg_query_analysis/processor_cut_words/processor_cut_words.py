import os
import threading
from dg_query_analysis.const.jiaba_posseg import FLAG_EN2CN
from dg_query_analysis.processor_base import ProcessorBase, Output, ParaError
from jieba import Tokenizer
from jieba.posseg import POSTokenizer
from dg_query_analysis.processor_stopwords.processor_stopwords import ProcessorStopwordsV73


class ProcessorCutWords(ProcessorBase):
    _pseg_dict = {}

    def __init__(self, *args, **kwargs):
        super(ProcessorCutWords, self).__init__(*args, **kwargs)
        self.lock = threading.RLock()
        self._cut_name = None
        self._proj = os.getenv("PROJ_NAME", "Pangu")

    def init(self, **kwargs):
        """
          Args:
              ``` dt ```                : class Tokenizer from jieba
              ``` user_dict_path ```    : user cut dict path
        """
        params = kwargs.get('params')
        self.lock.acquire()
        try:
            if self._cut_name not in self._pseg_dict:
                _cut = params.get('dt', None) or Tokenizer()
                user_dict_path = params.get('user_dict_path', None)
                if user_dict_path:
                    _cut.load_userdict(user_dict_path)

                self._pseg_dict[self._cut_name] = POSTokenizer(_cut)
            else:
                pass
        finally:
            self.lock.release()
        return self

    def _run_cut(self, **kwargs):
        params = kwargs.get('params')
        query = params.get('keyword')
        if not query:
            return []
        self._cut_name = "%s_%s" % (self._proj, params.get("app_name", "default"))  # todo：这里用到了pro 已解决
        if self._cut_name not in self._pseg_dict:
            self.init(**kwargs)

        _pseg = self._pseg_dict.get(self._cut_name, None)
        words = [w for w in _pseg.cut(query) if w.word.strip()]
        return words

    def run(self, **kwargs):
        params = kwargs.get('params')
        stopwords = params.get("stopwords", [])
        # 这里面不需要 所以不需要判断，只获取到就可以 或者不获取也可以
        new_params = kwargs.get('query_analysis_params', {})

        self.interaction = self.get_kwargs(new_params)
        p_cut_words_w_stopwords = self._run_cut(**kwargs)
        p_cut_words = [w for w in p_cut_words_w_stopwords if w.word not in stopwords]
        cut_words_w_stopwords = [w.word for w in p_cut_words_w_stopwords]
        cut_words = [e for e in cut_words_w_stopwords if e not in stopwords]
        return Output(p_cut_words_w_stopwords=p_cut_words_w_stopwords,
                      cut_words_w_stopwords=cut_words_w_stopwords,
                      p_cut_words=p_cut_words,
                      cut_words=cut_words)


class ProcessorCutWordsV70(ProcessorBase):
    _pseg_dict = {}

    def __init__(self, *args, **kwargs):
        super(ProcessorCutWordsV70, self).__init__(*args, **kwargs)
        self.lock = threading.RLock()
        self._cut_name = None
        self._proj = os.getenv("PROJ_NAME", "Pangu")

    def init(self, **kwargs):
        """
          Args:
              ``` dt ```                : class Tokenizer from jieba
              ``` user_dict_path ```    : user cut dict path
        """
        params = kwargs.get('params')
        self.lock.acquire()
        try:
            if self._cut_name not in self._pseg_dict:
                _cut = params.get('dt', None) or Tokenizer()
                user_dict_path = params.get('user_dict_path', None)
                if user_dict_path:
                    _cut.load_userdict(user_dict_path)

                self._pseg_dict[self._cut_name] = POSTokenizer(_cut)
            else:
                pass
        finally:
            self.lock.release()
        return self

    def _run_cut(self, **kwargs):
        params = kwargs.get('params')
        query = params.get('keyword')
        if not query:
            return []
        self._cut_name = "%s_%s" % (self._proj, params.get("app_name", "default"))
        if self._cut_name not in self._pseg_dict:
            self.init(**kwargs)

        _pseg = self._pseg_dict.get(self._cut_name, None)
        words = [w for w in _pseg.cut(query) if w.word.strip()]
        return words

    def _get_cut_flag(self, p_cut_words_w_stopwords):
        words = []
        lexicals = {}
        for e in p_cut_words_w_stopwords:
            words.append({"text": e.word, "lexical": e.flag})
            lexicals[e.flag] = FLAG_EN2CN.get(e.flag, e.flag)
        cut_flag = {"words": words,
                    "lexicals": lexicals}
        return cut_flag

    def _get_ner_flag(self, p_cut_words_w_stopwords, keyword):
        labels = []
        lexicals = {}
        for e in p_cut_words_w_stopwords:
            if e.flag in ["nr", "ns", "nt", "t", "nz", "mq"]:
                idx = keyword.find(e.word)
                offset = len(e.word)
                labels.append({"word": e.word,
                               "lexical": e.flag,
                               "index": idx,
                               "offset": offset})
                lexicals[e.flag] = FLAG_EN2CN.get(e.flag, e.flag)
        ner_flag = {"text": keyword,
                    "labels": labels,
                    "lexicals": lexicals}
        return ner_flag

    def run(self, **kwargs):
        params = kwargs.get('params')
        keyword = params.get("keyword")
        stopwords = params.get("stopwords", [])
        # 这里面不需要 所以不需要判断，只获取到就可以 或者不获取也可以
        new_params = kwargs.get('query_analysis_params', {})
        self.interaction = self.get_kwargs(new_params)
        p_cut_words_w_stopwords = self._run_cut(**kwargs)
        p_cut_words = [w for w in p_cut_words_w_stopwords if w.word not in stopwords]
        cut_words_w_stopwords = [w.word for w in p_cut_words_w_stopwords]
        cut_words = [e for e in cut_words_w_stopwords if e not in stopwords]
        stopwords_in_query = [e for e in cut_words_w_stopwords if e in stopwords]
        cut_flag = self._get_cut_flag(p_cut_words_w_stopwords)
        ner_flag = self._get_ner_flag(p_cut_words_w_stopwords, keyword)
        return Output(p_cut_words_w_stopwords=p_cut_words_w_stopwords,
                      cut_words_w_stopwords=cut_words_w_stopwords,
                      p_cut_words=p_cut_words,
                      cut_words=cut_words,
                      stopwords_in_query=stopwords_in_query,
                      cut_flag=cut_flag,
                      ner_flag=ner_flag)


class ProcessorCutWordsV73(ProcessorBase):
    _pseg_dict = {}
    _pseg_dict_version = {}

    def __init__(self, *args, **kwargs):
        super(ProcessorCutWordsV73, self).__init__(*args, **kwargs)
        self.lock = threading.RLock()
        self._cut_name = None
        self._proj = os.getenv("PROJ_NAME", "Pangu")

    def init(self, version, **kwargs):
        """
          Args:
              ``` dt ```                : class Tokenizer from jieba
              ``` user_dict_path ```    : user cut dict path
        """
        params = kwargs.get('params')
        search_core = params.get("search_core")
        core_type = params.get('core_type')

        words_dict = self._get_various_types_words(search_core, core_type, params)
        self.lock.acquire()
        try:
            if self._cut_name not in self._pseg_dict or self._pseg_dict_version.get(self._cut_name, -1) != version:
                _cut = params.get('dt', None) or Tokenizer()
                user_dict_path = params.get('user_dict_path', None)
                if user_dict_path:
                    _cut.load_userdict(user_dict_path)
                for word_type in words_dict:
                    for word in words_dict[word_type]:
                        _cut.add_word(*word)
                self._pseg_dict[self._cut_name] = POSTokenizer(_cut)
                self._pseg_dict_version[self._cut_name] = version

        finally:
            self.lock.release()
        return self

    @staticmethod
    def _add_words_ner(word_list, character, weight=10):
        ner_list = []
        for word in set(word_list):
            ner_list.append((word.lower(), weight, character))
        return ner_list

    def _get_stop_words(self, params):
        params['g_rds_client'] = self.rds
        params['g_rds_mapping_dao'] = self.g_rds_mapping_dao
        words_processor = ProcessorStopwordsV73().run(params=params)
        stop_li = words_processor.get("stopwords", [])
        stop_words = self._add_words_ner(stop_li, "stop")
        return stop_words

    def _get_person_words(self, search_core, core_type):
        bind_card_type = self.g_rds_mapping_dao.get_person_dict_ids(search_core, core_type)
        person_li = self.g_rds_mapping_dao.get_card_person_info(search_core) if "person" in bind_card_type else []
        person_words = self._add_words_ner(person_li, "nr", 11)
        return person_words

    def _get_phrase_words(self, search_core, core_type):
        dict_id_list = self.g_rds_mapping_dao.get_phrase_dict_ids(search_core, core_type)
        if not dict_id_list or not len(dict_id_list):
            return []
        phrase_li = self.g_rds_mapping_dao.get_phrase_info(dict_id_list)
        phrase_words = self._add_words_ner(phrase_li, "phrase")
        return phrase_words

    def _get_various_types_words(self, search_core, core_type, params):
        words_dict = {}
        if self._cut_name == "%s:jieba:%s" % (self._proj, "default"):
            return words_dict
        words_dict["stop"] = self._get_stop_words(params)
        words_dict["person"] = self._get_person_words(search_core, core_type)
        words_dict["phrase"] = self._get_phrase_words(search_core, core_type)
        return words_dict

    def _is_change_word_dict(self):
        version = self.g_rds_mapping_dao.get_jieba_core_version(self._cut_name)
        if version is None:
            self._cut_name = "%s:jieba:%s" % (self._proj, "default")
            return -1
        return int(version)

    def _run_cut(self, **kwargs):
        params = kwargs.get('params')
        query = params.get('keyword')
        if not query:
            return []
        search_core = params.get("search_core")
        core_type = params.get('core_type')
        app_name = params.get("app_name")
        if not all([search_core, core_type, app_name]):
            self._cut_name = "%s:jieba:%s" % (self._proj, "default")
        else:
            self._cut_name = "%s:jieba:%s:%s" % (self._proj, app_name, search_core)
        version = self._is_change_word_dict()
        if self._cut_name not in self._pseg_dict or self._pseg_dict_version.get(self._cut_name, -1) != version:
            self.init(version, **kwargs)

        _pseg = self._pseg_dict.get(self._cut_name, None)
        words = [w for w in _pseg.cut(query) if w.word.strip()]
        return words

    def _get_cut_flag(self, p_cut_words_w_stopwords):
        words = []
        lexicals = {}
        for e in p_cut_words_w_stopwords:
            words.append({"text": e.word, "lexical": e.flag})
            lexicals[e.flag] = FLAG_EN2CN.get(e.flag, e.flag)
        cut_flag = {"words": words,
                    "lexicals": lexicals}
        return cut_flag

    def _get_ner_flag(self, p_cut_words_w_stopwords, keyword):
        labels = []
        lexicals = {}
        for e in p_cut_words_w_stopwords:
            if e.flag in ["nr", "ns", "nt", "t", "nz", "mq", "phrase"]:
                idx = keyword.find(e.word)
                offset = len(e.word)
                labels.append({"word": e.word,
                               "lexical": e.flag,
                               "index": idx,
                               "offset": offset})
                lexicals[e.flag] = FLAG_EN2CN.get(e.flag, e.flag)
        ner_flag = {"text": keyword,
                    "labels": labels,
                    "lexicals": lexicals}
        return ner_flag

    def _get_words_type(self, params, p_cut_words_w_stopwords):
        keyword = params.get("keyword")
        cut_words_w_stopwords, phrase, stopwords_in_query, cut_words, p_cut_words = [], set(), [], [], []
        stopwords = {w.word for w in p_cut_words_w_stopwords if w.flag == "stop"}
        for w in p_cut_words_w_stopwords:
            if w.word in stopwords:
                stopwords_in_query.append(w.word)
            else:
                cut_words.append(w.word)
                p_cut_words.append(w)
            if w.flag == "phrase":
                phrase.add(w.word)
            cut_words_w_stopwords.append(w.word)
        cut_flag = self._get_cut_flag(p_cut_words_w_stopwords)
        ner_flag = self._get_ner_flag(p_cut_words_w_stopwords, keyword)
        return dict(p_cut_words_w_stopwords=p_cut_words_w_stopwords,
                    cut_words_w_stopwords=cut_words_w_stopwords,
                    stopwords=list(stopwords),
                    phrase=list(phrase),
                    p_cut_words=p_cut_words,
                    cut_words=cut_words,
                    stopwords_in_query=stopwords_in_query,
                    cut_flag=cut_flag,
                    ner_flag=ner_flag)

    def run(self, **kwargs):

        params = kwargs.get("params", {})
        new_params = kwargs.get('query_analysis_params', {})
        self.interaction = self.get_kwargs(new_params)
        self.g_rds_mapping_dao = self.interaction[2]
        self.rds = self.interaction[1]
        # 这里需要用到g_rds_mapping_dao对象，做判断
        try:
            if not self.g_rds_mapping_dao:
                raise ParaError("CutWords_V73 g_rds_mapping_dao类未找到, 请传入g_rds_mapping_dao关键字参数")
            if not self.rds:
                # 因为类内部用了stopwords类，所以这里还是需要获取rds类
                raise ParaError("CutWords_V73 rds类未找到, 请传入g_rds_client关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        p_cut_words_w_stopwords = self._run_cut(**kwargs)
        cut_words_dict = self._get_words_type(params, p_cut_words_w_stopwords)
        return Output(**cut_words_dict)
