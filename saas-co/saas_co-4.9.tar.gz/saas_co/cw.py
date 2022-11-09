from jsonpath_ng import parse
from .paginate import cw_paginate

#####################################

class get_metric_data(cw_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('MetricDataResults[*]')
