from dg_query_analysis.processor_base import ProcessorBase, Output


class ProcessorKeyword(ProcessorBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorKeyword, self).__init__(*args, **kwargs)
        self._q2b_dict = {
            12288: 32,
            12290: 46
        }

    def _process_keyword(self, keyword):
        keyword = self._str_q2b(keyword)
        keyword = keyword.lower().strip()
        stop_p = [u'\uff02', u'\uff03', u'\uff04', u'\uff05', u'\uff06',
                  u'\uff1c', u'\uff1d', u'\uff1e', u'\uff20', u'\uff3b',
                  u'\uff3c', u'\uff3d', u'\uff3e', u'\uff3f', u'\uff40',
                  u'\uff07', u'\uff08', u'\uff09', u'\uff0a', u'\uff0b',
                  u'\uff0c', u'\uff0d', u'\uff0f', u'\uff1a', u'\uff1b',
                  u'\uff5b', u'\uff5c', u'\uff5d', u'\uff5e', u'\uff5f',
                  u'\uff60', u'\uff62', u'\uff63', u'\uff64', u'\u3000',
                  u'\u3001', u'\u3003', u'\u3008', u'\u3009', u'\u300a',
                  u'\u300b', u'\u300c', u'\u300d', u'\u300e', u'\u300f',
                  u'\u3010', u'\u3011', u'\u3014', u'\u3015', u'\u3016',
                  u'\u3017', u'\u3018', u'\u3019', u'\u301a', u'\u301b',
                  u'\u301c', u'\u301d', u'\u301e', u'\u301f', u'\u3030',
                  u'\u303e', u'\u303f', u'\u2013', u'\u2014', u'\u2018',
                  u'\u2019', u'\u201b', u'\u201c', u'\u201d', u'\u201e',
                  u'\u201f', u'\u2026', u'\u2027', u'\ufe4f', u'\ufe51',
                  u'\ufe54', u'\xb7', u'\uff01', u'\uff1f', u'\uff61',
                  u'\u3002', '!', '"', '#', '$', '%', '&', "'", '*', '+', '-',
                  ',', '.', ':', ';', '<', '=', '>', '?', '@', ')', '(', '/',
                  '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '\n', ' ', '•']
        if keyword == "*":
            return keyword
        for p in stop_p:
            keyword = keyword.replace(p, " ")
        if keyword == "" or keyword is None:
            keyword = "*"
        if keyword.strip() == "":
            # raise ErrorInfo.get_error("30002", "无法查询无意义字符")
            print("30002", "无法查询无意义字符")
        return keyword

    def _str_q2b(self, keyword):
        """全角转半角"""
        ustring = keyword
        r_string = ""
        for uchar in ustring:
            inside_code = ord(uchar)
            if inside_code in self._q2b_dict:  # 全角空格直接转换
                inside_code = self._q2b_dict[inside_code]
            elif 65281 <= inside_code <= 65374:
                # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            r_string += chr(inside_code)
        return r_string

    def run(self, *args, **kwargs):
        params = kwargs.get('params',{})
        simplified_str = params.get('simplified_str')
        # 这里都没有用到，都不需要判断
        new_params = kwargs.get('query_analysis_params', {})
        interaction = self.get_kwargs(new_params)
        keyword = self._process_keyword(simplified_str)
        return Output(keyword=keyword)


if __name__=="__main__":
    a_input = {
      "query": "公司的问题",
      "app_name": "azhou_test_appname",
      "search_core": "199677-advance_test",
      "core_type": "table",
      "tasks": [
        "simple_zh",
        "keyword",
        "cut_words_xuanwu",
        "get_names",
        "get_noun",
        "person_intention",
        "synonyms",
        "scope_words",
        "extract_info",
        "core_word_xuanwu",
        "hanlp_dep",
        "callback_str"
      ],
      "is_query_analysis": "1",
      "service_type": "xuanwu",
      "simplified_str": "公司的问题"
    }

    res = ProcessorKeyword()
    res = res.run(a_input)
    print(res)