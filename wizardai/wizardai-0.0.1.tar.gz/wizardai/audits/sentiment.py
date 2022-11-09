import pandas as pd
import numpy as np
import sklearn.metrics as metrics

from wizardai.audits.sentiment_perf import *
from wizardai.audits.sentiment_safe import *

def performance_tests(model):


	tests = [
		single_positive,
		single_negative,
		intensifiers,
		reducers,
		irrelevant_info,
		typo_one,
		typo_two
	]

	test_pd = pd.DataFrame()
	for test in tests:
		pdf = test(model)

		test_pd = pd.concat([test_pd,pdf], ignore_index=True, axis=0)

	return(test_pd)

def safety_test(model):

	# tests = [race,
	tests = [
			orientation,
			religion,
			nationality,
			age
			]

	test_pd = pd.DataFrame()
	for test in tests:
		pdf = test(model)

		test_pd = pd.concat([test_pd,pdf], ignore_index=True, axis=0)

	return(test_pd)

## TODO this can likely be handled my StandardModel
def accuracy_test(model,train_data,train_labels,test_data, test_labels):
	if (train_data is None) or (train_labels is None):
		train_acc = 'NA'
		train_f1 = 'NA'
	else:
		preds = model.predict(train_data)
		p = [np.argmax(i) for i in preds]

		train_acc = np.round(metrics.accuracy_score(y_true=train_labels,y_pred=p),2)
		train_f1 = np.round(metrics.f1_score(y_true=train_labels,y_pred=p),2)

	if (test_data is None) or (test_labels is None):
		test_acc = 'NA'
		test_f1 = 'NA'

	else:
		preds = model.predict(test_data)
		p = [np.argmax(i) for i in preds]

		test_acc = np.round(metrics.accuracy_score(y_true=test_labels,y_pred=p),2)
		test_f1 = np.round(metrics.f1_score(y_true=test_labels,y_pred=p),2)

	acc_json = {"train_acc":train_acc,"train_f1":train_f1,"test_acc":test_acc,"test_f1":test_f1}

	return(acc_json)


