import random as 랜덤
from 함수 import * 

def 숫자무작위(숫자시작: 숫자함수, 숫자끝: 숫자함수):
    return 랜덤.randint(숫자시작, 숫자끝)

def 글자무작위(*글자고르기: 글자함수):
    return 랜덤.choice(글자고르기)
