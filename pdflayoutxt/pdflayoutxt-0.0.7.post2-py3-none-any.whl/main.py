import pdfplumber
from cleantext import clean
from autocorrect import Speller
import re
import os
import traceback
from .utils import *
from functools import partial

class pdfextracter:
    def __init__(self) -> None:
        pass

    def get_pdf_text(self,pdf_path,pdf_password="",pages=[],left_most_x=0,left_most_y=0,right_most_x=1,right_most_y=1):
        try:
            if os.path.isfile(pdf_path):
                if pdf_path.endswith(".pdf") or  pdf_path.endswith(".PDF"):
                        self.textpages=self.extract_pdf_text(pdf_path,password=pdf_password,pages=pages,crop=(left_most_x,left_most_y,right_most_x,right_most_y)) 
                        # allpagecleaned=list(map(clean_text,textpages))
                        self.allpagecleaned=[self.clean_pdf_text(i) for i in self.textpages]
                        print("self.allpagecleaned")
                        print(self.allpagecleaned)
                        return self.allpagecleaned
                else:
                    raise InvalidFileFormat("We only support .pdf or .PDF",os.path.splitext(pdf_path)[-1])
            else:
                raise FileNotFoundError("Input file path is not correct. Please check and pass the correct path")
            
        except Exception as e:
            print(traceback.print_exc(limit=None, file=None, chain=True))
            
        
            
    def extract_pdf_text(self,pdf_path,password="",pages=[],crop=(0,0,1,1)):
        self.textpages_=[]
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
                    self.textpages_.append(croppedpage.extract_text(layout=True))
                    
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
                self.textpages_.append(croppedpage.extract_text(layout=True))
                
            else:
                raise InvalidPageNumbers("Pages argument can only be a list like [1,2,3,4] or an integer like 1",pages)   
            
        return self.textpages_
            

    def clean_pdf_text(self,pagewise):
        lines=pagewise.splitlines()
        self.j=[]
        for i1 in lines:
            if i1.strip()!="":
                new_string = i1.encode('ascii',errors='ignore').decode()
                self.j.append(new_string.strip())
        print("JJJ")
        print(self.j)
        self.cleanedlines=list(map(partial(clean, stemming=False,stopwords=False,clean_all=False),self.j))
        print("cleanedlines")
        print(self.cleanedlines)
        self.spell = Speller(lang='en',fast=True,only_replacements=True)
        self.outputcleanedlines=[]
        for i in self.cleanedlines:
            sen=re.sub("[^a-zA-Z0-9 ][@_!#$%^&*()<>?/\|}{~:]", "",self.spell(i))
            # sen=spell(i)
            if len(sen)>3:
                self.outputcleanedlines.append(sen)
        print("outputcleanedlines")
        print(self.outputcleanedlines)
        return self.outputcleanedlines






if __name__=="__main__":
    pdfpath=r"../../../Beginning Interviewing.pdf"
    j=pdfextracter()
    print(j.get_pdf_text(pdfpath))
