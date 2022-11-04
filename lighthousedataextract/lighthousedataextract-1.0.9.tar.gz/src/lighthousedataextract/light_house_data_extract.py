from jsonpath_ng import jsonpath, parse
import pandas as pd
import os
import json
from collections import OrderedDict

class LightHouseDataExtract:

    def __init__(self, path_to_json='./report/lighthouse/',url_category_file=None,from_api=False):

       self.jsonpath_page_size = parse("$.audits.total-byte-weight")
       self.jsonpath_first_contentful_paint = parse("$.audits.first-contentful-paint")
       self.jsonpath_largest_contentful_paint = parse("$.audits.largest-contentful-paint")
       self.jsonpath_first_meaningful_paint = parse("$.audits.first-meaningful-paint")
       self.jsonpath_speed_index = parse("$.audits.speed-index")
       self.jsonpath_total_blocking_time = parse("$.audits.total-blocking-time")
       self.jsonpath_max_potential_fid = parse("$.audits.max-potential-fid")
       self.jsonpath_server_response_time = parse("$.audits.server-response-time")
       self.jsonpath_interactive = parse("$.audits.interactive")
       self.jsonpath_score = parse("$.categories.performance.score")
       self.jsonpath_network_resources =  parse("$.audits.network-requests.details.items")
       self.jsonpath_audit = parse("$.audits.audit_name")

       self.path_to_json = path_to_json 
       self.json_files = [path_to_json+pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json') and 'summary' not in  pos_json ]
       self.from_api= from_api
       self.url_category_file = url_category_file
       self.url_category = self.find_url_category_dict()
       self.category="other"
       self.url = ""
       self.fetch_time = 0.0
       self.lh_perf_metrics_data = []
       self.opportunities_data = [] 
       self.diagnostics_data = []
       self.resources_data = []
       self.network_resources = []
       self.report = self.get_report()

    def find_url_category_dict(self):
        result = {}
        if self.url_category_file!=None:
           df = pd.read_csv(self.url_category_file,names=['url', 'category'], header=None)
           result = OrderedDict(zip(df['url'], df['category']))
        return result

    def df_report(self):
        df = pd.DataFrame(self.lh_perf_metrics_data, columns = ['url','fetch_time','category','page_size','score','first_contentful_paint','largest_contentful_paint','first_meaningful_paint','speed_index','total_blocking_time','max_potential_fid','server_response_time','interactive'])
        return df
    def df_opportunities(self):
        df = pd.DataFrame(self.opportunities_data,columns=['url','fetch_time','category','audit_text','estimated_savings'])
        return df
    def df_diagnostics(self):
        df = pd.DataFrame(self.diagnostics_data,columns=['url','fetch_time','category','diagnostic_id','label','value'])
        return df
    def df_resources(self):
        df = pd.DataFrame(self.resources_data,columns=['url','fetch_time','category','resource_url','resource_type','startTime','endTime'])
        return(df)

    def get_report(self):
        for file in self.json_files:
            with open(file) as f:
                 self.report = json.load(f)  
                 if self.from_api:
                    self.report = self.report['lighthouseResult']
            self.find_lh_perf_metrics_data()
            self.find_opportunities_data()
            self.find_diagnostics_data()
            self.find_resources_data()
 
    def find_lh_perf_metrics_data(self): 
        lh_perf_metrics_data=[]
        self.url= self.report['requestedUrl']
        self.fetch_time = self.report['fetchTime']
        page_size = 0.0
        score = 0.0
        first_contentful_paint = 0.0
        largest_contentful_paint = 0.0
        first_meaningful_paint = 0.0
        speed_index = 0.0
        total_blocking_time = 0.0
        max_potential_fid = 0.0
        server_response_time = 0.0
        interactive = 0.0
        if self.url_category_file!=None:
           self.category = self.url_category.get(self.url,"other")
        try:
           page_size = [match.value['numericValue'] for match in self.jsonpath_page_size.find(self.report) ][0]
           page_size = page_size / 1024
           score = [match.value for match in self.jsonpath_score.find(self.report) ][0]
           first_contentful_paint = [match.value['numericValue'] for match in self.jsonpath_first_contentful_paint.find(self.report) ][0]
           largest_contentful_paint = [match.value['numericValue'] for match in self.jsonpath_largest_contentful_paint.find(self.report) ][0]
           first_meaningful_paint = [match.value['numericValue'] for match in self.jsonpath_first_meaningful_paint.find(self.report) ][0]
           speed_index = [match.value['numericValue'] for match in self.jsonpath_speed_index.find(self.report) ][0]
           total_blocking_time = [match.value['numericValue'] for match in  self.jsonpath_total_blocking_time.find(self.report) ][0]
           max_potential_fid = [match.value['numericValue'] for match in self.jsonpath_max_potential_fid.find(self.report) ][0]
           server_response_time = [match.value['numericValue'] for match in self.jsonpath_server_response_time.find(self.report) ][0]
           interactive = [match.value['numericValue'] for match in self.jsonpath_interactive.find(self.report) ][0]
           self.network_resources = [match.value for match in self.jsonpath_network_resources.find(self.report) ]
        except:
           pass 
        lh_perf_metrics_data=[self.url,self.fetch_time,self.category,page_size,score,first_contentful_paint,largest_contentful_paint,first_meaningful_paint,speed_index,total_blocking_time,max_potential_fid,server_response_time,interactive]
        self.lh_perf_metrics_data.append(lh_perf_metrics_data)

    def find_opportunities_data(self): 
        saving_opportunities = [];
        for audit_name in self.report['audits']:
           audit = self.report['audits'][audit_name]
           if 'details' in audit:
               if (audit['details']['type'] == 'opportunity'):
                  saving_opportunities.append({
                   'audit_text': audit['title'],
                    'estimated_savings': audit['details']['overallSavingsMs']
                  })
        for opportunity in saving_opportunities:
            self.opportunities_data.append([self.url,self.fetch_time,self.category,opportunity['audit_text'],opportunity['estimated_savings']])
 
    def find_diagnostics_data(self): 
        diagnostics = []
        current_list_of_items = []
        if (self.report['audits']['mainthread-work-breakdown']['score'] != 1 and self.report['audits']['mainthread-work-breakdown']['score'] != None) :
            for item in self.report['audits']['mainthread-work-breakdown']['details']['items'] :
                current_list_of_items.append({
              		'label': item['groupLabel'],
              		'value': item['duration']
            		})
    
        diagnostics.append({
      		'diagnostic_id': 'mainthread-work-breakdown',
        	'items': current_list_of_items,
    		})

        current_list_of_items = []
        if (self.report['audits']['bootup-time']['score'] != 1 and self.report['audits']['bootup-time']['score'] != None):
           for item in self.report['audits']['bootup-time']['details']['items']: 
                current_list_of_items.append({
             	       'label': item['url'],
                       'value': item['total']
                })
      
        diagnostics.append({
           'diagnostic_id': 'bootup-time',
           'items': current_list_of_items,
           })

        current_list_of_items = [];
        if (self.report['audits']['font-display']['score'] != 1 and self.report['audits']['font-display']['score'] != None):
           for item in self.report['audits']['font-display']['details']['items']:
               current_list_of_items.append({
                      'label': item['url'],
                      'value': item['wastedMs']
               })

        diagnostics.append({
           'diagnostic_id': 'font-display',
           'items': current_list_of_items,
        });

        current_list_of_items = [];
        if (self.report['audits']['third-party-summary']['score'] != 1 and self.report['audits']['third-party-summary']['score'] != None):
           for item in self.report['audits']['third-party-summary']['details']['items']:
               current_list_of_items.append({
                 'label': item['entity']['text'],
                 'value': item['blockingTime']
               })
          
        diagnostics.append({
            'diagnostic_id': 'third-party-summary',
            'items': current_list_of_items,
          })

        current_list_of_items = [];
        if (self.report['audits']['dom-size']['score'] != 1 and self.report['audits']['dom-size']['score'] != None) :
           for item in self.report['audits']['dom-size']['details']['items']:
               if isinstance(item['value'], str):
                  current_list_of_items.append({
                    'label': item['statistic'],
                    'value': float(item['value'].replace(',', ''))
                   })
               else:
                   current_list_of_items.append({
                    'label': item['statistic'],
                    'value': float(item['value'])
                   })
        diagnostics.append({
          'diagnostic_id': 'dom-size',
          'items': current_list_of_items,
        })

        for diagnostic in diagnostics:
            diagnostic_id = diagnostic['diagnostic_id']
            for item in diagnostic['items']:
                self.diagnostics_data.append([self.url,self.fetch_time,self.category,diagnostic['diagnostic_id'],item['label'],item['value']])

    def find_resources_data(self):
        resource_chart_data = [ ] 
        for resource in self.network_resources: 
            for item in resource:
                resource_type= item.get('resourceType',None)
                if resource_type != None:
                   resource_type = item['resourceType']
                else:
                   resource_type = 'Other'
                if 'startTime' in item and 'endTime' in item:    
                    self.resources_data.append([self.url,self.fetch_time,self.category,item['url'],resource_type,item['startTime'],item['endTime']])

