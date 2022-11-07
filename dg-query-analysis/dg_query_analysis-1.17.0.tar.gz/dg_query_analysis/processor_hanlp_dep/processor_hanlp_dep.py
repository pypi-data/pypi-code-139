import requests
import json
import time
from collections import defaultdict
from dg_query_analysis.const.hanlp_dep import DEP_DICT, DEP_COLOR_DICT
from dg_query_analysis.processor_base import ProcessorBase, Output, Input, ParaError

class ProcessorHanlpDep(ProcessorBase):
    def __init__(self, **kwargs):
        super(ProcessorHanlpDep, self).__init__(**kwargs)

    @staticmethod
    def _get_dep_params(params: Input):
        keyword = params.get("keyword")
        return dict(keyword=keyword)

    def hanlp_dep(self, query):
        result = {}
        try:
            url = f"{self.config.ML_SERVER}pangu_hanlp?sentence={query}"
            begin = time.time()
            res = requests.request("GET", url)
            ret = json.loads(res.content)
            result = ret.get("result", {})
            end = time.time()
            print("hanlp_dep request consumes: %s, url: %s, result: %s"
                            % (end - begin, url, res.content))
        except Exception as e:
            print("hanlp_dep request err: %s" % e)
        return result

    def _get_dep_list(self, keyword):
        dep_flag = {"entities": [],
                    "relations": [],
                    "sentence": keyword,
                    "options": {
                        "depends": []
                    }}
        if keyword:
            dep_ret = self.hanlp_dep(keyword)
            relations_dict = defaultdict(list)
            relations = []
            depends = []
            entities = [{"word": "root",
                         "type": ""}]
            for idx in range(len(dep_ret.get("dep", []))):
                relations_dict[dep_ret["dep"][idx][1]].append([(idx+1), dep_ret["dep"][idx][0]])
            for idx in range(len(dep_ret.get("tok/fine", []))):
                entities.append({"word": dep_ret["tok/fine"][idx],
                                 "type": dep_ret["pos/pku"][idx]})
            for k in relations_dict:
                relations.append({"type": k,
                                  "collections": relations_dict[k]})
                depends.append({"type": k,
                                "intro": DEP_DICT[k],
                                "color": DEP_COLOR_DICT[k]})
            dep_flag = {"entities": entities,
                        "relations": relations,
                        "sentence": keyword,
                        "options": {
                            "depends": depends
                        }}
        return dep_flag

    def run(self, *args, **kwargs):
        params = kwargs.get("params", {})
        is_query_analysis = params.get("is_query_analysis")
        if is_query_analysis not in ['1', 1]:
            return Output()

        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        self.config = interaction[0]
        # 这里需要用到config对象，做判断
        try:
            if not self.config:
                raise ParaError("HanlpDep config类未找到, 请传入config关键字参数")
            if not self.config.ML_SERVER:
                raise ParaError("HanlpDep config中缺少ML_SERVER关键字")
        except Exception as e:
            print("引发异常：", repr(e))
            return Output(error=repr(e))
        dep_params = self._get_dep_params(params)
        dep_flag = self._get_dep_list(**dep_params) or []
        return Output(dep_flag=dep_flag)

# rds, rec_, config,