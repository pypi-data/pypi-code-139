import pandas as pd
import numpy as np
from pymongo import MongoClient

from wizardai.audits.preflight import *

## This could be a conditional load based on the audit type
import wizardai.audits.sentiment as sentiment

# TODO add testcase level for fairness
def process_tests(t_pdf,subgroups=False,examples=False):
    
    t_pdf['totalimpact'] = [np.nan if t == None else t['totalimpact'] for t in t_pdf.testscore ]
    t_pdf['totalimpact_abs'] = np.abs(t_pdf['totalimpact'])
    failrate_pdf = t_pdf.groupby('category').agg({"testresult":"sum","category":"count"})
    failrate_pdf['fail_rate'] = 1-failrate_pdf.testresult/failrate_pdf.category
    failrate_pdf['num_cases'] = failrate_pdf.category
    failrate_pdf.drop(["testresult","category"],axis=1,inplace=True)

    fail_pdf = t_pdf[~t_pdf.testresult]
    impact_pdf = fail_pdf.groupby('category')[['totalimpact_abs','totalimpact']].mean()
    impact_pdf.rename(columns={"totalimpact_abs":"fail_impact","totalimpact":"avg_bias"},inplace=True)

    result_pdf = failrate_pdf.join(impact_pdf)

    result_pdf['risk_level'] = 'Low'
    result_pdf.loc[(result_pdf.fail_rate>0.1)|(result_pdf.fail_impact>0.1),'risk_level'] = 'Moderate'
    result_pdf.loc[(result_pdf.fail_rate>0.1)&(result_pdf.fail_impact>0.1),'risk_level'] = 'High'

    results_dict = {
    "score":100*(1-result_pdf.fail_rate.mean()-result_pdf.fail_impact.mean()),
    "tests": list(result_pdf.index)
    }
    
    for group in results_dict['tests']:
        results_dict[group] = result_pdf.loc[group].to_dict()

    if subgroups:
        
        failrate_pdf = t_pdf.groupby('testcase').agg({"testresult":"sum","testcase":"count","category":"max"})
        failrate_pdf['fail_rate'] = 1-failrate_pdf.testresult/failrate_pdf.testcase
        failrate_pdf.drop(["testresult","testcase"],axis=1,inplace=True)

        impact_pdf = fail_pdf.groupby('testcase')[['totalimpact_abs','totalimpact']].mean()
        impact_pdf.rename(columns={"totalimpact_abs":"fail_impact","totalimpact":"avg_bias"},inplace=True)

        case_pdf = failrate_pdf.join(impact_pdf)

        for group in results_dict['tests']:
            results_dict[group]['subgroups'] = case_pdf[case_pdf.category==group][['fail_rate','fail_impact','avg_bias']].to_dict()
            
    if examples:
        
        for group in results_dict['tests']:
            fail_group = fail_pdf[fail_pdf.category == group]
            pass_group = t_pdf[(t_pdf.testresult)&(t_pdf.category == group)]
            
            if len(fail_group) == 0:
                fail_examples = "NA"
            else:
                fail_examples = fail_group.sample(min([3,len(fail_group)]))[['testinput','testoutput','testscore']].to_json()
                
                
            if len(pass_group) == 0:
                pass_examples = "NA"
            else:
                pass_examples = pass_group.sample(min([3,len(pass_group)]))[['testinput','testoutput','testscore']].to_json()
            
            results_dict[group]['examples'] = {"pass":pass_examples,"fail":fail_examples}
        

    return(results_dict)

def initialize_database(username,password):

    ## Assumes all run on cluster0
    try:
        client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.dnioijx.mongodb.net/?retryWrites=true&w=majority")
        z = client.server_info()
    except:
        raise Exception('Unable to connect to Wizard AI. Contact the friendly folks at support@thewizard.ai for help')
    
    return(client)

def upload_report_data(client,model_json):

    Collection = client.data["model_audits"]
    Collection.insert_one(model_json)

    return True

## TODO, need to process
    ## train_data
    ## labels
    ## test_data
    ## model_name
    ## audit_type
    ## owner

## TODO handling .predict() functions is going to be a problem

## do I want to make this a dictionary?

## TODO: Process here and send json, or pandas/csv loading into app for in-app processing?
    ## Pros:
        # Can pull examples easily
        # Can extend analysis
        # Can export tests
    ## Cons:
        # Take longer to process
        # Need to refactor code

def build_report(user_model, username, password, 
                    audit_type=None, model_name=None, owner=None, 
                    train_data=None,  train_labels=None, 
                    test_data=None, test_labels=None, 
                    tokenizer=None, preprocessor=None,
                    open_report=True):

    mongo_client = initialize_database(username,password)

    model = StandardModel(  user_model=user_model,  audit_type=audit_type,  model_name=model_name, owner=owner, 
                            train_data=train_data,  train_labels=train_labels, 
                            test_data=test_data,    test_labels=test_labels, 
                            tokenizer=tokenizer,    preprocessor=preprocessor)

    print("Running Full Audit...")

    ## TODO Make this a full function // page if there is interest
    print("\t Accuracy Tests...")
    if train_data == train_data:
        acc_json = sentiment.accuracy_test(model,train_data,train_labels,test_data,test_labels)
    else:
        print("\t\t(skipping)")

    print("\t Performance Tests...")
    perf_pdf = sentiment.performance_tests(model)
    perf_json = process_tests(perf_pdf, examples=True)
    print(f"\t\t{len(perf_pdf):,} tests cases completed.")

    print("\t Safety Tests...")
    safe_pdf = sentiment.safety_test(model)
    safe_json = process_tests(safe_pdf, subgroups=True)
    print(f"\t\t{len(safe_pdf):,} tests cases completed.")

    audit_dict = {
        "model_name":model.name,
        "model_type": model.audit_type,
        "audit_date": str(datetime.now()),
        "audit_owner": model.owner,
        "safety": safe_json,
        "performance":perf_json,
        "accuracy": acc_json,
        "acc": acc_json['train_acc'],
        "f1": acc_json['train_f1']
    }


    report_upload_status = upload_report_data(mongo_client,audit_dict)

    if open_report:
        # TODO: selenium login?
        # TODO: print link (with auth?)
    else:
        print(f"Model Report Upload Status: {report_upload_status}")
    return
