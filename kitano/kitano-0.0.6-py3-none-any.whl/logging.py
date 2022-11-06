# ReinanBr 04/10/22
# lib: kitano
# LICENSE: MIT

from datetime import datetime
import time




#get date


def getDate(strfitTime:str='[%H:%M:%S %d/%m/%Y]') -> None:
	datePrint = datetime.now().strftime(strfitTime)
	return datePrint


showDate = True
#show date
def show_date(argument:bool) -> None:
	global showDate
	showDate = argument

#strft
strft = None
def strPrt(strf:str=None) -> None:
	global strft
	strft = strf


'''
#lib for pritting
def puts(*txt,sep=' '):
	textShowing = ''
	if len(txt) > 1:
		textShowing = (sep).join([str(text) for text in txt])
	if showDate:
		if strft:
			datePrt = getDate(strf)
		else:
			datePrt = getDate()
		prtTxt = f'{datePrt}: {textShowing}'
	else:
		prtTxt = f'{textShowing}'

	print(prtTxt)


'''



''' class Puts'''
class Puts:
	
	def __init__(self):
	  self.allDate = False
	  self.showDate = True
	  self.strfDate = False
	  self.sep = ' '
	  #pass
	#lib for pritting
	def puts(self,*txt):
	  textShowing = txt
	  if len(txt) > 1:
	    textShowing = (self.sep).join([str(text) for text in txt])
	  if self.showDate:
	    if self.strfDate:
	      datePrt = getDate(self.strfDate)
	      prtTxt = f'{datePrt}: {textShowing}'
	    else:
	      datePrt = getDate('[%H:%m:%S %d/%m]')
	      prtTxt = f'{datePrt}: {textShowing}'
	  else:
	    prtTxt = f'{textShowing}'
	  print(prtTxt)
