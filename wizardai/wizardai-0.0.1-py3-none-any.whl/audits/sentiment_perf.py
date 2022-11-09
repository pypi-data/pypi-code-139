from wizardai.audits.preflight import synth_data
from itertools import compress
import pandas as pd
import numpy as np
import string


## THE GOAL OF ALL OF THESE FUNCTIONS IS TO RUN TESTS AND OUTPUT A PDF
## POST PROCESSING FOR REPORT HAPPENS ELSEWHERE

"""
test outcomes | pdf
	category   | "Intensifier"
	testcase   | word
	testinput  | inputs, input pairs
	testoutput | model output
	testscore  | impact score
	testresult | pass/fail

"""


## TODO Add check to ensure model_func can make batch predictions
## TODO update pdf in single pos/neg functions
## TODO Consider "separation_score" -- tracking the difference between classes with prediction
	## [0.8,0.2] -> [0.6,0.5] has a decrease separation score
	## Does impact score capture this?
## Consider highlighint if sentence is pos/neg in int/red cases



def single_positive(model):
	"""
    Parameters
    ---------
    model: model to pentest

    Output
    -------
    - failure rate
	- failure words
	- test outcomes
	"""

	s = synth_data()

	i = s['pos_adj']+s['pos_verb_present']+s['pos_verb_past']

	preds =  model.predict(i)

	score = [np.argmax(i) for i in preds]
	results = [i == 1 for i in score]

	sp_pd = pd.DataFrame({"category":"Single Positive",
						  "testcase":i,
						  'testinput': i,
						  'testoutput': list(preds),
						  'testscore': None,
						  'testresult': results})
	
	return(sp_pd)

def single_negative(model):
	"""
    Parameters



    ---------
    model: model to pentest

    Output
    -------
    - failure rate
	- failure words
	- test outcomes
	"""

	s = synth_data()
	i = s['neg_adj']+s['neg_verb_present']+s['neg_verb_past']

	preds =  model.predict(i)

	score = [np.argmax(i) for i in preds]
	results = [i == 0 for i in score]

	sp_pd = pd.DataFrame({"category":"Single Negative",
						  "testcase":i,
						  'testinput': i,
						  'testoutput': list(preds),
						  'testscore': None,
						  'testresult': results})
	
	return(sp_pd)

## IN THE FUTURE WE CAN ADD INTESIFIERS TO YOUR DATASET ITSELF
def intensifiers(model):
	"""
    Parameters
    ---------
    model: model to pentest

    Output
    -------
    - failure rate | 0.06
	- failure words | list of str
	- test outcomes | pdf
		category   | "Intensifier"
		testcase   | intensifier
		testinput  | inputs pairs
		testoutput | model output
		testscore  | impact score
		testresult | pass/fail

	"""

	# Checking the "impact score" of intensifiers. Should be >0

	s = synth_data()

	og_inputs = []
	ints_inputs = []
	testcase = []
	labels = []

	for pos_verb in s['pos_verb_present']:
		for int_adv in s['int_adv']:
			if np.random.choice([True,False]):
				og = f"I {pos_verb} my {np.random.choice(s['profs'])}."
			else:
				og = f"I {pos_verb} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}."
			
			i = og.split(pos_verb)[0]+int_adv+' '+pos_verb+og.split(pos_verb)[1]
			
			testcase.append(int_adv)
			labels.append(1)

			og_inputs.append(og)
			ints_inputs.append(i)


	# TODO ADD NEG WORDS
	for pos_verb in s['neg_verb_present']:
		for int_adv in s['int_adv']:
			if np.random.choice([True,False]):
				og = f"I {pos_verb} my {np.random.choice(s['profs'])}."
			else:
				og = f"I {pos_verb} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}."
			
			i = og.split(pos_verb)[0]+int_adv+' '+pos_verb+og.split(pos_verb)[1]
			
			testcase.append(int_adv)
			labels.append(0)

			og_inputs.append(og)
			ints_inputs.append(i)

	# Pred
	og_preds =  model.predict(og_inputs)
	int_preds =  model.predict(ints_inputs)

	scores = []
	result = []

	for idx in range(len(labels)):
		l = labels[idx]
		og = og_preds[idx]
		ints =  int_preds[idx]
		
		n = ints[0]-og[0]
		p = ints[1]-og[1]

		imp_score = p-n if l else n-p
		r = True if imp_score>-0.1 else False
		
		result.append(r)
		scores.append({"posimpact":p,"negimpact":n,"totalimpact":p-n}) #[p,n,imp_score])


	# wrong_idx = [not i in for in result]
	# fail_rate = np.sum(wrong_idx)/len(result)
	# fail_examples =  list(compress(inputs, wrong_idx))

	## TODO output raw predictions
	pdf = pd.DataFrame({"category":"Intensifiers",
		"testcase":testcase,
		"testinput":[[i,j] for i,j in zip(og_inputs,ints_inputs)],
		"testoutput": [[i,j] for i,j in zip(og_preds,int_preds)],
		"testscore":scores,
		"testresult":result})
	
	return(pdf)


def reducers(model):
	"""
    Parameters
    ---------
    model: model to pentest

    Output
    -------
    - failure rate | 0.06
	- failure words | list of str
	- test outcomes | pdf
		category   | "Intensifier"
		testcase   | intensifier
		testinput  | inputs pairs
		testoutput | model output
		testscore  | impact score
		testresult | pass/fail

	"""

	# Checking the "impact score" of intensifiers. Should be >0

	s = synth_data()

	og_inputs = []
	ints_inputs = []
	testcase = []
	labels = []

	for pos_verb in s['pos_verb_present']:
		for int_adv in s['red_adv']:
			if np.random.choice([True,False]):
				og = f"I {pos_verb} my {np.random.choice(s['profs'])}."
			else:
				og = f"I {pos_verb} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}."
			
			i = og.split(pos_verb)[0]+int_adv+' '+pos_verb+og.split(pos_verb)[1]
			
			testcase.append(int_adv)
			labels.append(1)

			og_inputs.append(og)
			ints_inputs.append(i)


	for neg_verb in s['neg_verb_present']:
		for int_adv in s['red_adv']:
			if np.random.choice([True,False]):
				og = f"I {neg_verb} my {np.random.choice(s['profs'])}."
			else:
				og = f"I {neg_verb} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}."
			
			i = og.split(neg_verb)[0]+int_adv+' '+neg_verb+og.split(neg_verb)[1]
			
			testcase.append(int_adv)
			labels.append(0)

			og_inputs.append(og)
			ints_inputs.append(i)

	# Pred
	og_preds =  model.predict(og_inputs)
	int_preds =  model.predict(ints_inputs)

	scores = []
	result = []

	for idx in range(len(labels)):
		l = labels[idx]
		og = og_preds[idx]
		ints =  int_preds[idx]
		
		n = ints[0]-og[0]
		p = ints[1]-og[1]

		imp_score = p-n if l else n-p
		r = True if imp_score<0.1 else False
		
		result.append(r)
		scores.append({"posimpact":p,"negimpact":n,"totalimpact":imp_score}) #[p,n,imp_score])


	# wrong_idx = [not i in for in result]
	# fail_rate = np.sum(wrong_idx)/len(result)
	# fail_examples =  list(compress(inputs, wrong_idx))

	## TODO output raw predictions
	pdf = pd.DataFrame({"category":"Reducers",
		"testcase":testcase,
		"testinput":[[i,j] for i,j in zip(og_inputs,ints_inputs)],
		"testoutput": [[i,j] for i,j in zip(og_preds,int_preds)],
		"testscore":scores,
		"testresult":result})
	
	return(pdf)

## TODO Add real data
## TODO label doesn't matter, just if it changes prediction
def irrelevant_info(model):
	
	## TODO make this better
	def random_string():
	    return(''.join(np.random.choice([x for x in string.ascii_letters], np.random.randint(1,10))))
	
	def random_tenure():
	    return(f"I have been using Wizard AI for {np.random.randint(1,100)} years")
	
	def random_url():
	    n = np.random.randint(1,15)
	    extention = ''.join(np.random.choice([x for x in string.ascii_letters + string.digits], n))
	    return("Check out my blog: https://t.co/" + extention)


	## Get rid of this function in future
	s = synth_data()

	og_inputs = []
	irr_inputs = []

	for _ in range(250):
		
		pos = np.random.choice([True,False])
		p = s['pos_verb_past'] if pos else s['neg_verb_past']
		v = np.random.choice(p)

		l = 1 if pos else 0

		og = f"I {v} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}. "
		irr = np.random.choice([random_string(),random_tenure(),random_url()])+'. '

		front = np.random.choice([True,False])
		irr_sent = irr+og if front else og+irr

		og_inputs.append(og)
		irr_inputs.append(irr_sent)
	
	# Pred
	og_preds =  model.predict(og_inputs)
	irr_preds =  model.predict(irr_inputs)

	scores = []
	result = []

	for idx in range(len(og_inputs)):
		og   = 	og_preds[idx]
		irr =  irr_preds[idx]
		
		n = irr[0]-og[0]
		p = irr[1]-og[1]

		if np.abs(p-n)>0.1 or np.abs(n-p)>0.1:
			r = False
		else:
			r = True
		
		result.append(r)
		scores.append({"posimpact":p,"negimpact":n, "totalimpact":p-n})

	## TODO output raw predictions
	pdf = pd.DataFrame({"category":"Irrelevance",
		"testcase":"NA",
		"testinput":[[i,j] for i,j in zip(og_inputs,irr_inputs)],
		"testoutput": [[i,j] for i,j in zip(og_preds,irr_preds)],
		"testscore":scores,
		"testresult":result})
	
	return(pdf)

## TODO Add real data
def typo_one(model):
	
	s = synth_data()

	og_inputs = []
	typo_inputs = []

	for _ in range(250):
		
		pos = np.random.choice([True,False])
		p = s['pos_verb_past'] if pos else s['neg_verb_past']
		v = np.random.choice(p)

		l = 1 if pos else 0

		og = f"I {v} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}. "
		i = np.random.random_integers(len(og)-2)
		t_1 = og[i]
		t_2 = og[i+1]
		typo = og[:i]+t_2+t_1+og[i+2:]

		og_inputs.append(og)
		typo_inputs.append(typo)
		

	# Pred
	og_preds =  model.predict(og_inputs)
	typo_preds =  model.predict(typo_inputs)

	scores = []
	result = []

	for idx in range(len(og_inputs)):
		og   = 	og_preds[idx]
		typo =  typo_preds[idx]
		
		n = typo[0]-og[0]
		p = typo[1]-og[1]

		if np.abs(p-n)>0.1 or np.abs(n-p)>0.1:
			r = False
		else:
			r = True

		result.append(r)
		scores.append({"posimpact":p,"negimpact":n, "totalimpact":p-n})

	## TODO output raw predictions
	pdf = pd.DataFrame({"category":"One Typo",
		"testcase":"NA",
		"testinput":[[i,j] for i,j in zip(og_inputs,typo_inputs)],
		"testoutput": [[i,j] for i,j in zip(og_preds,typo_preds)],
		"testscore":scores,
		"testresult":result})

	return(pdf)

## TODO Add real data
def typo_two(model):

	s = synth_data()

	og_inputs = []
	typo_inputs = []

	for _ in range(250):
		
		pos = np.random.choice([True,False])
		p = s['pos_verb_past'] if pos else s['neg_verb_past']
		v = np.random.choice(p)

		l = 1 if pos else 0

		og = f"I {v} {np.random.choice(s['it']).lower()} {np.random.choice(s['nouns'])}. "
		i1,i2 = np.random.random_integers(len(og)-2,size=2)
		t_1 = og[i1]
		t_2 = og[i1+1]
		typo = og[:i1]+t_2+t_1+og[i1+2:]

		t_1 = og[i2]
		t_2 = og[i2+1]
		typo = og[:i2]+t_2+t_1+og[i2+2:]

		og_inputs.append(og)
		typo_inputs.append(typo)
		

	# Pred
	og_preds =  model.predict(og_inputs)
	typo_preds =  model.predict(typo_inputs)

	scores = []
	result = []

	for idx in range(len(og_inputs)):
		og   = 	og_preds[idx]
		typo =  typo_preds[idx]
		
		n = typo[0]-og[0]
		p = typo[1]-og[1]

		if np.abs(p-n)>0.1 or np.abs(n-p)>0.1:
			r = False
		else:
			r = True

		result.append(r)
		scores.append({"posimpact":p,"negimpact":n, "totalimpact":p-n})

	## TODO output raw predictions
	pdf = pd.DataFrame({"category":"Two Typos",
		"testcase":"NA",
		"testinput":[[i,j] for i,j in zip(og_inputs,typo_inputs)],
		"testoutput": [[i,j] for i,j in zip(og_preds,typo_preds)],
		"testscore":scores,
		"testresult":result})

	return(pdf)


def shap(model):
	return









