from dg_query_analysis.processor_base import ProcessorBase, Output, Input


class ProcessorNormalNoun(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorNormalNoun, self).__init__(**kwargs)

    @staticmethod
    def _get_noun_params(params: Input):
        p_cut_words = params.get("p_cut_words")
        if not p_cut_words:
            # raise ErrorInfo.get_error("30001", "cut words or query lost")
            print("30001", "cut words or query lost")
        return dict(p_cut_words=p_cut_words)

    @staticmethod
    def _get_normal_noun(p_cut_words):
        normal_noun = []
        noun_flags = ['n', 'nz', 'nl', 'ng']
        noun_flags = set(noun_flags)
        for idx, item in enumerate(p_cut_words):
            if item.flag in noun_flags and len(item.word) > 1:
                normal_noun.append(item.word)
        return normal_noun

    def run(self, *args, **kwargs):
        params = kwargs.get("params", {})
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        noun_params = self._get_noun_params(params)
        normal_noun = self._get_normal_noun(**noun_params) or []
        return Output(normal_noun=normal_noun)

