from datetime import datetime

## TODO: If there are flags in the literal .predict function I am 
##       not sure what to do...
## TODO: Accept different model predict functions than .predict()
## TODO: Loads of tests...
	## - If it can handle batch processing
class StandardModel:

	def __init__(self, user_model, audit_type=None, model_name=None, owner=None, 
                    train_data=None,  train_labels=None, 
                    test_data=None,   test_labels=None,
                    tokenizer=None, preprocessor=None):

		if not has_predict_func(user_model):
			raise Exception("Currently can only handle models with a .predict() function")
		
		self.model        = user_model
		self.tokenizer    = tokenizer
		self.preprocessor = preprocessor

		self.audit_type = audit_type
		# self.name = model_name if model_name else "model_"+str(datetime.now()).replace(" ","_")
		self.name       = model_name if model_name else "temp_model3"
		self.owner 		= owner 
		self.train_data     = train_data 
		self.train_labels  	= train_labels
		self.test_data      = test_data 
		self.test_labels  	= test_labels


	def predict(self,input_values):
		
		i = input_values
		if self.preprocessor:
			i = self.preprocessor(i)
		if self.tokenizer:
			i = self.tokenizer(i)

		return(self.model.predict(i))


## HELPER FUNCTIONS


"""
Returns dict with keys:
profs | professions
nouns | nouns
neu_adjs | neutral adj
pos_adj | positive adj
pos_verb_present | positive present tense verbs
pos_verb_past | positive past tense verbs
neg_adj
neg_verb_present
neg_verb_past
it | The/This/That
be | is/was
int_adv | intensifier adverbs
red_adv | reducer adverbs
"""

## TODO: Check if one of the neutral words has a bias in the model...
def synth_data():
	"""
	For now this is dumb.
	But in the future this will take words from input data
	And create similar synthetic sentences
	"""

	e = dict()

	profs = ['accountant','actor','artist','barber'
	'billionaire', 'biologist', 'boy', 'boyfriend',
	'businessman', 'cashier','celebrity','character', 'chef',
	'child', 'coach','comedian', 'cop',
	'dad', 'dentist', 'developer','doctor', 'dog', 'engineer',
	'fan', 'farmer', 'father', 'fighter', 'fisherman','friend',
	'guy', 'girl', 'girlfriend', 'historian','journalist', 'judge', 'lawyer',
	'magician', 'man', 'mathematician', 'monk',
	'musician', 'nerd', 'novelist','nurse','painter', 'pastor', 
	'pharmacist','philosopher', 'physicist','pilot', 'plumber',
	'poet', 'policeman','politician', 'preacher', 'priest', 'prophet',
	'psychiatrist', 'psychologist', 'reader', 'rebel', 'receptionist',
	'refugee', 'reporter', 'saint','secretary','senator'
	'soldier', 'son', 'student', 'superhero', 'survivor',
	'teacher', 'terrorist' 'vet', 'wizard','writer']
	e['profs'] = profs

	nouns = ['mall', 'housing','role','problem','storage',
	   'solution','examination','shirt','tea','skill',
	   'assignment','music','math','platform','literature',
	   'pizza', 'refrigerator','transportation','establishment','oven']
	e['nouns'] = nouns

	neu_adj = ['normal','unbiased', 'neutral',
	    'evenhanded','impartial', 'unprejudiced ',
	   'uninfluenced', 'ordinary','everyday', 'regular',
	   'expected','conventional', 'common']
	e['neu_adj'] = neu_adj

	pos_adj = ['good', 'great', 'excellent', 'amazing', 'extraordinary',
			'beautiful', 'fantastic', 'nice', 'incredible', 'exceptional',
			'awesome', 'perfect', 'fun', 'happy', 'adorable', 'brilliant',
			'exciting', 'sweet', 'wonderful']
	e['pos_adj'] = pos_adj

	pos_verb_present = ['like', 'enjoy', 'appreciate', 'love',
					'recommend', 'admire', 'value', 'welcome']
	e['pos_verb_present'] = pos_verb_present

	pos_verb_past = ['liked', 'enjoyed', 'appreciated',
				'loved', 'admired', 'valued', 'welcomed']
	e['pos_verb_past'] = pos_verb_past

	neg_adj = ['awful', 'bad', 'horrible', 'weird', 'rough', 'lousy', 'unhappy',
	           'average', 'difficult', 'poor', 'sad', 'frustrating', 'hard',
	           'lame', 'nasty', 'annoying', 'boring', 'creepy', 'dreadful',
	           'ridiculous', 'terrible', 'ugly', 'unpleasant']
	e['neg_adj'] = neg_adj


	neg_verb_present = ['hate', 'dislike', 'regret',  'abhor', 'dread', 'despise' ]
	e['neg_verb_present'] = neg_verb_present

	neg_verb_past = ['hated', 'disliked', 'regretted',  'abhorred', 'dreaded', 'despised']
	e['neg_verb_past'] = neg_verb_past

	it = ['The', 'This', 'That']
	e['it'] = it

	be = ['is', 'was']
	e['be'] = be

	int_adv = ['very', 'really', 'absolutely', 'truly', 'extremely', 
	          'quite', 'incredibly', 'amazingly', 'especially', 
	          'exceptionally', 'unbelievably', 'utterly', 'exceedingly', 
	          'rather', 'totally', 'particularly','definitely','certainly',
	          'genuinely','strongly','sincerely', 'significantly']

	e['int_adv'] = int_adv

	red_adv = ['somewhat', 'kinda', 'mostly', 'probably', 'generally', 
	           'reasonably','slightly', 'sort of','kind of','marginally',
	           'apprehensively','trepidatiously']

	e['red_adv'] = red_adv

	return(e)


def has_predict_func(model):
	## TODO make this better

	return('predict' in dir(model))


