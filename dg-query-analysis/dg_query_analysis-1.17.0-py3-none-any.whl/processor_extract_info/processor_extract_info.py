import query_toolkits as qt
from dg_query_analysis.processor_base import ProcessorBase, Output

class ProcessorExtractInfo(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorExtractInfo, self).__init__(**kwargs)

    @staticmethod
    def _get_extract_info_params(**kwargs):
        params = kwargs.get('params')
        simplified_str = params.get('simplified_str')
        p_cut_words = params.get('p_cut_words_w_stopwords')
        return dict(simplified_str=simplified_str, p_cut_words=p_cut_words)

    @staticmethod
    def _analysis_extract_info(simplified_str, p_cut_words):
        time_words = qt.extract_time(simplified_str, p_cut_words)
        number_words = qt.extract_number(p_cut_words)
        requirement_words = qt.extract_requirement(p_cut_words)
        return dict(time_words=time_words, number_words=number_words, requirement_words=requirement_words)

    def run(self, **kwargs):
        params = kwargs.get("params", {})
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        extract_info_params = self._get_extract_info_params(**kwargs)
        extract_info = self._analysis_extract_info(**extract_info_params)
        return Output(**extract_info)
