from dg_query_analysis.processor_base import ProcessorBase, Output, Input


class ProcessorName(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorName, self).__init__(**kwargs)

    @staticmethod
    def _get_name_params(params: Input):
        query = params.get('query')
        p_cut_words = params.get("p_cut_words")
        if not (p_cut_words and query):
            print("30001", "cut words or query lost")
        return dict(query=query, p_cut_words=p_cut_words)


    @staticmethod
    def _get_possible_names(p_cut_words):
        names = []
        name_flags = ['nr', 'nrt', 'nrfg']
        name_flags = set(name_flags)
        for idx, item in enumerate(p_cut_words):
            if item.flag in name_flags:
                names.append((item.word, idx))
        return names

    @staticmethod
    def _merge_names(names, query):
        l_names = len(names)
        if l_names == 1:
            return [names[0][0]]

        r_index = zip(range(l_names - 1), range(1, l_names))
        merged_names = []
        for start, end in r_index:
            if names[end][1] - names[start][1] == 1:
                merged_name = "%s%s" % (names[start][0], names[end][0])
                if merged_name in query:
                    merged_names.append(merged_name)
                else:
                    merged_names.append(names[start][0])
                    if end == l_names - 1:
                        merged_names.append(names[end][0])
            else:
                merged_names.append(names[start][0])
                if end == l_names - 1:
                    merged_names.append(names[end][0])
        return merged_names

    def get_names(self, query, p_cut_words):
        try:
            names = self._get_possible_names(p_cut_words)
            merged_names = self._merge_names(names, query)
            return merged_names
        except Exception as e:
            print("analysis name error")
        return None

    def run(self, *args, **kwargs):
        params = kwargs.get("params", {})
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        name_params = self._get_name_params(params)
        names = self.get_names(**name_params) or []
        return Output(names=names)

