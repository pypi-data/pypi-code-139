from dg_query_analysis.utils.driver import traditional_to_simplified
from dg_query_analysis.processor_base import ProcessorBase, Input, Output


class ProcessorTraditional(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorTraditional, self).__init__(**kwargs)

    def process_traditional(self, query):
        simplified_str = query
        try:
            simplified_str = traditional_to_simplified.convert(query)
        except Exception as e:
            print("upload process traditional error: %s" % e)
        return simplified_str

    def run(self, *args, **kwargs):
        params = kwargs.get('params', {})
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        query = params.get("query", "")
        if not query:
            return Output()
        simplified_str = self.process_traditional(query)
        return Output(simplified_str=simplified_str)


