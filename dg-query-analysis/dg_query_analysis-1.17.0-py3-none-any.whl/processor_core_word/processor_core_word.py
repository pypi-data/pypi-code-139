from dg_query_analysis.processor_base import ProcessorBase, Output, Input

class ProcessorCoreWord(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorCoreWord, self).__init__(**kwargs)

    @staticmethod
    def _get_core_word_params(params: Input):
        p_cut_words = params.get("p_cut_words")
        if not p_cut_words:
            print("30001", "cut words or query lost")
        return dict(p_cut_words=p_cut_words)

    @staticmethod
    def _get_core_word(p_cut_words):
        normal_noun = []
        noun_flags = ['i', 'nr', 'n', 'nz', 'nl', 'ng', 'nrfg', 'nrt', 'ns', 'nt']
        noun_flags = set(noun_flags)
        for idx, item in enumerate(p_cut_words):
            if item.flag in noun_flags and len(item.word) > 1:
                normal_noun.append(item.word)
        return normal_noun

    def run(self, *args, **kwargs):
        params = kwargs.get("params", {})
        new_params = kwargs.get('query_analysis_params', {})
        # 这里也没有看到用法，所以rds和config也是只获取，不判断
        self.interaction = self.get_kwargs(new_params)
        core_word_params = self._get_core_word_params(params)
        core_word = self._get_core_word(**core_word_params) or []
        return Output(core_word=core_word)

class ProcessorCoreWordV73(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorCoreWordV73, self).__init__(**kwargs)

    @staticmethod
    def _get_core_word_params(params: Input):
        p_cut_words = params.get("p_cut_words")
        phrase = params.get("phrase", [])
        synonyms = params.get("synonyms", {})
        normal = params.get("normal_noun", [])
        names = params.get("names", [])
        scope = params.get("scope_words", {})
        if not p_cut_words:
            raise ErrorInfo.get_error("30001", "cut words or query lost")
        return dict(p_cut_words=p_cut_words, phrase=phrase, synonyms_dict=synonyms,
                    normal=normal, names=names, scopes=scope)

    @staticmethod
    def _get_core_word(p_cut_words, phrase, synonyms_dict, normal, names, scopes):
        analysis_phrase_sys_names = {
            "phrase_words": {},
            "names_words": {},
            "normal_words": {},
            "synonyms_words": {}
        }
        normal_noun = []
        noun_flags = ['i', 'ns', 'nt']
        noun_flags = set(noun_flags)
        analysis_phrase_sys_names["synonyms_words"].update(synonyms_dict)
        synonyms = analysis_phrase_sys_names["synonyms_words"]
        for scope in scopes:
            synonyms[scope] = set(synonyms[scope] + scopes[scope]) if scope in synonyms else set(scopes[scope])

        for idx, item in enumerate(p_cut_words):
            if item.flag in noun_flags and len(item.word) > 1:
                normal_noun.append(item.word)
            if item.word in phrase and len(item.word) > 1:
                normal_noun.append(item.word)
                analysis_phrase_sys_names["phrase_words"][item.word] = list(set(synonyms.pop(item.word, set())) | {item.word})
            elif item.word in names and len(item.word) > 1:
                normal_noun.append(item.word)
                analysis_phrase_sys_names["names_words"][item.word] = list(set(synonyms.pop(item.word, set())) | {item.word})
            elif item.word in normal and len(item.word) > 1:
                normal_noun.append(item.word)
                analysis_phrase_sys_names["normal_words"][item.word] = list(set(synonyms.pop(item.word, set())) | {item.word})

        return normal_noun, analysis_phrase_sys_names

    def run(self, *args, **kwargs):
        """
        Args:
            **kwargs: params
        Returns: Output
        core_word 后续词分析时会使用到核心词展示，在不影响词分析展示情况下，进行dsl核心词的一些定制化分析。
        """
        params = kwargs.get("params", {})
        new_params = kwargs.get('query_analysis_params', {})
        # 这里也没有看到用法，所以rds和config也是只获取，不判断
        self.interaction = self.get_kwargs(new_params)
        core_word_params = self._get_core_word_params(params)
        core_word, analysis_words = self._get_core_word(**core_word_params) or ([], {})
        return Output(core_word=core_word, analysis_phrase_sys_names=analysis_words)
