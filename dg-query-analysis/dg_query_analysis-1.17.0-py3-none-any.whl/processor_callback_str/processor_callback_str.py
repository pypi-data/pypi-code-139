from dg_query_analysis.processor_base import ProcessorBase, Output, Input


class ProcessorCallbackStr(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorCallbackStr, self).__init__(**kwargs)

    @staticmethod
    def _get_params(params: Input):
        synonyms_dict = params.get("synonyms", {})
        cut_words = params.get("cut_words", [])
        scope_words = params.get("scope_words", {})
        if not cut_words:
            print("30001", "cut words or query lost")
        return dict(cut_words=cut_words, synonyms_dict=synonyms_dict, scope_dict=scope_words)

    @staticmethod
    def _analysis_callback_str(synonyms_dict, scope_dict, cut_words):
        cut_words = cut_words.copy()
        extend_words = []
        for k in synonyms_dict:
            extend_words.append(k)
            extend_words += synonyms_dict[k]
        for i in scope_dict:
            extend_words.append(i)
            extend_words += scope_dict[i]
        callback_str = ' '.join(cut_words)
        for w in extend_words:
            w_list = w.split("/")
            for _w in w_list:
                if _w in cut_words or not _w.strip():
                    continue
                callback_str += " " + _w
                cut_words.append(_w)
        return callback_str

    def run(self, *args, **kwargs):
        """
        Args:
            **kwargs: params
        Returns: Output
        core_word 后续词分析时会使用到核心词展示，在不影响词分析展示情况下，进行dsl核心词的一些定制化分析。
        """
        params = kwargs.get("params", {})
        # 这里面不需要 所以不需要判断，只获取到就可以 或者不获取也可以
        new_params = kwargs.get('query_analysis_params',{})
        interaction = self.get_kwargs(new_params)
        analysis_params = self._get_params(params)
        _callback_str = self._analysis_callback_str(**analysis_params) or ''
        # callback_str 全部字段需要召回高亮的词，callback_str_dict针对字段需要召回高亮的词
        return Output(callback_str=_callback_str, callback_str_dict={})



if __name__ == '__main__':
    # p = ProcessorCoreWord()
    p = ProcessorCallbackStr()
    data = {'param':Input(synonyms={'a':'aa'}, cut_words={'b':'bb'})}
    print(p.run(params=data))