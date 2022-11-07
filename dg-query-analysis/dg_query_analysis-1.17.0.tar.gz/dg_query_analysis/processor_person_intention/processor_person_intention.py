from dg_query_analysis.processor_base import ProcessorBase, Output, Input


class ProcessorPersonIntention(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorPersonIntention, self).__init__(**kwargs)

    @staticmethod
    def _get_person_intention_params(params: Input):
        query = params.get("query")
        names = params.get("names", [])
        if not query:
            print("30001", "cut words or query lost")
        return dict(query=query, names=names)

    @staticmethod
    def _get_person_intention(query, names):
        if names:
            return True
        person_intention_words = ["人", "师", "士", "民", "员"]
        if any(word in query for word in person_intention_words):
            return True

        return False

    def run(self, *args, **kwargs):
        params = kwargs.get("params", {})
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        person_intention_params = self._get_person_intention_params(params)
        is_person_intention = self._get_person_intention(**person_intention_params) or []
        return Output(is_person_intention=is_person_intention)

