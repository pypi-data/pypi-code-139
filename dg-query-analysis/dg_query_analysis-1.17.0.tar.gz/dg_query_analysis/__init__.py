# import os,sys
# os.chdir(sys.path[0])



from dg_query_analysis import processor_callback_str
from dg_query_analysis import processor_core_word
from dg_query_analysis import processor_cut_phrase
from dg_query_analysis import processor_cut_words
from dg_query_analysis import processor_extract_info
from dg_query_analysis import processor_hanlp_dep
from dg_query_analysis import processor_keyword
from dg_query_analysis import processor_name
from dg_query_analysis import processor_normal_noun
from dg_query_analysis import processor_person_intention
from dg_query_analysis import processor_scope_words
from dg_query_analysis import processor_simple_zh
from dg_query_analysis import processor_stock_recog
from dg_query_analysis import processor_stopwords
from dg_query_analysis import processor_synonyms

# __all__ = [
#     "ProcessorCallbackStr",
#     "ProcessorCoreWord",
#     "ProcessorCoreWordV73",
#     "ProcessorCutPhrase",
#     "ProcessorCutPhraseV70",
#     "ProcessorCutWords",
#     "ProcessorCutWordsV70",
#     "ProcessorCutWordsV73",
#     "ProcessorExtractInfo",
#     "ProcessorHanlpDep",
#     "ProcessorKeyword",
#     "ProcessorName",
#     "ProcessorNormalNoun",
#     "ProcessorPersonIntention",
#     "ProcessorStockRecog",
#     "ProcessorStopwords",
#     "ProcessorStopwordsV73",
#     "ProcessorSynonyms",
#     "ProcessorScope",
#     "ProcessorTraditional",
# ]
__all__= ['processor_core_word',
         'processor_cut_phrase',
         'processor_simple_zh',
         'processor_scope_words',
         'processor_name',
         'processor_extract_info',
         'processor_callback_str',
         'processor_stock_recog',
         'processor_normal_noun',
         'processor_keyword',
         'processor_synonyms',
         'processor_cut_words',
         'processor_stopwords',
         'processor_hanlp_dep',
         'processor_person_intention']