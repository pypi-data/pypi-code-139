from pydantic import *

class __함수__(BaseModel):
    __숫자__ = int
    __글자__ = str
    __소숫점__ = float

def 숫자함수(숫자: __함수__.__숫자__):
    return int(숫자)

def 글자함수(글자: __함수__.__글자__):
    return str(글자)

def 소숫점함수(소숫점: __함수__.__소숫점__):
    return float(소숫점)
