import pdfplumber
from cleantext import clean
from autocorrect import Speller
import re
import os
import traceback
from .utils import *

def get_text(pdf_path,pdf_password="",pages=[],left_most_x=0,left_most_y=0,right_most_x=1,right_most_y=1):
    try:
        if os.path.isfile(pdf_path):
            if pdf_path.endswith(".pdf") or  pdf_path.endswith(".PDF"):
                    textpages=extract_text(pdf_path,password=pdf_password,pages=pages,crop=(left_most_x,left_most_y,right_most_x,right_most_y)) 
                    allpagecleaned=list(map(clean_text,textpages))
                    return allpagecleaned
            else:
                raise InvalidFileFormat("We only support .pdf or .PDF",os.path.splitext(pdf_path)[-1])
        else:
            raise FileNotFoundError("Input file path is not correct. Please check and pass the correct path")
        
    except Exception as e:
        print(traceback.print_exc(limit=None, file=None, chain=True))
        
    
        
def extract_text(pdf_path,password="",pages=[],crop=(0,0,1,1)):
    textpages_=[]
    with pdfplumber.open(pdf_path,password=password) as pdf:

        if isinstance(pages,list):
            if len(pages)==0:
                pages=list(range(len(pdf.pages)))
            for i in pages:
                page = pdf.pages[int(i)]
                width=page.width
                height=page.height
                a,b,c,d=crop
                if a<=1:
                    a=a*width
                if b<=1:
                    b=b*height
                if c<=1:
                    c=c*width
                if d<=1:
                    d=d*height
                croppedpage = page.crop((a,b,c,d))
                textpages_.append(croppedpage.extract_text(layout=True))
                
        elif isinstance(pages,int):
            page=pdf.pages[pages]
            width=page.width
            height=page.height
            a,b,c,d=crop
            if a<=1:
                a=a*width
            if b<=1:
                b=b*height
            if c<=1:
                c=c*width
            if d<=1:
                d=d*height
            croppedpage = page.crop((a,b,c,d))
            textpages_.append(croppedpage.extract_text(layout=True))
            
        else:
            raise InvalidPageNumbers("Pages argument can only be a list like [1,2,3,4] or an integer like 1",pages)   
        
    return textpages_
        

def clean_text(pagewise):
    lines=pagewise.split("\n")
    j=[]
    for i in lines:
        if i.strip()!="":
            j.append(i)
    cleanedlines=list(map(clean,j))
    spell = Speller(lang='en',fast=True)
    outputcleanedlines=[]
    for i in cleanedlines:
        sen=re.sub("[^a-zA-Z0-9 ][@_!#$%^&*()<>?/\|}{~:]", "",spell(i))
        if len(sen)>3:
            outputcleanedlines.append(sen)
    return outputcleanedlines








