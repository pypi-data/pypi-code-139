#!/usr/bin/python3
# -*- coding: utf-8 -*-
from dg_query_analysis.processor_base import ProcessorBase, Output, ParaError



class ProcessorStockRecog(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorStockRecog, self).__init__(*args, **kwargs)

        pass

    def _stock_info_analysis(self, query):
        if not query:
            return []
        stocks = self._stock_recog.stock_name_ac.get_tags(query) + self._stock_recog.stock_id_ac.get_tags(
            query) + self._stock_recog.stock_initials_ac.get_tags(query)
        return stocks

    def run(self, **kwargs):
        params = kwargs.get('params')
        query = params.get("query", "")
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        self._stock_recog = interaction[3]
        # 这里需要用到g_rds_mapping_dao对象，做判断
        try:
            if not self._stock_recog:
                raise ParaError("StockRecog stock_recog类未找到, 请传入StockRecog关键字参数")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        stock_result = self._stock_info_analysis(query)
        return Output(stock_result=stock_result)


