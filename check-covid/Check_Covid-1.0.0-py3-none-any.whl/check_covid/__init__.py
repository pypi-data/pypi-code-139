from time import time, sleep
starting_time = time()
from pyautogui import leftClick, hotkey, press
from pyperclip import copy, paste
from datetime import datetime, timedelta
import pyautogui
pyautogui.PAUSE = 0
NAME_FIELD = [500, 256]
PASS_FIELD = [500, 383]
BUTTON_POS = [325, 478]
DAYS       = int(input("Ammount of days to search? "))
INCL_TODAY = input("Search for today? y/n ").lower()=='y'
delay      = 0.1
def ctrl(key): hotkey('ctrl', key); sleep(delay)
def enter_field(position, data):
    leftClick(*position)
    ctrl('a')
    press('backspace')
    copy(str(data))
    ctrl('v')
def fill_form(name, passport_ID):
    enter_field(NAME_FIELD, name)
    enter_field(PASS_FIELD, passport_ID)
    leftClick(*BUTTON_POS)
    sleep(delay)
def query():
    ctrl('a')
    ctrl('c')
    sleep(delay)
    return paste()
def process_data(data):
    data = data.split('服务说明:')[0].split('查询')[-1].strip()
    data = [i.strip() for i in data.split('\n')]
    tests = []
    for i in range(len(data)//8):
        tests.append({
            'time':   data[8*i+1],
            'test':   data[8*i+5],
            'result': data[8*i+7],
        })
    return tests
def check_data(tests, time_stamps):
    error = False
    if len(tests)<3:
        print(f'You only completed {len(tests)} out of {len(time_stamps)}!!!')
        error = True
    for test in tests:
        if test['test']=="检测中":
            # Nobody Cares
            continue
        if test['test']!="核酸":
            print(f'Hmm, why did you test for {test["test"]} '
                  f'instead of 核酸?')
            error = True
        if test['result']!="【阴性】":
            print(f'You tested {test["result"]} '
                  f'instead of 【阴性】!!!')
            error = True
    times = [test['time'].split(' ')[0] for test in tests
             if test['test'] == "核酸" and
             test['result'] == "【阴性】" and
             test['time'] != "检测中"]
    for time_stamp in time_stamps:
        if time_stamp not in times:
            print(f'You didn\'t do testing on {time_stamp}!!!')
            error = True
    return error
def get_time_stamps():
    stamps = []
    today = datetime.now()
    z = 0 if INCL_TODAY else 1
    for day in range(z, DAYS+z):
        stamps.append(today-timedelta(days=day))
    return stamps
def process_time_stamps(stamps):
    return [str(stamp).split(' ')[0] for stamp in stamps]
def check(name, passport_ID):
    fill_form(name, passport_ID)
    z = query(); data = process_data(z)
    print(f'Checking {name}')
    while data==[]: print("BRUH"); fill_form(name, passport_ID); z = query(); data = process_data(z)
    failed = check_data(data,process_time_stamps(get_time_stamps()))
    if failed: print(f'{name} failed the test!!!')
    return failed
def pretty_join(array):
    if len(array) == 0: return 'none'
    if len(array) == 1: return array[0]
    if len(array) == 2: return f'{array[0]} and {array[1]}'
    if len(array)  > 2: return ', '.join(array[:-1]) + \
                               ', and ' + array[-1]
def main(data):
    failed = []
    count = 1
    for entry in data:
        if check(*entry): failed.append(entry[0])
        print(f'Done {count}/{len(data)}!!!')
        count+=1
    print(f'{len(failed)} failed',end='')
    if failed: print(f': {pretty_join(failed)}')
    else: print("\nHOORAY!!!")
setup_time = time()-starting_time
data = open(input('Drag file here and enter >>> ').strip()).read()
while '  ' in data: data = data.replace('  ',' ')
while '\n\n' in data: data = data.replace('\n\n','\n')
while '\t\t' in data: data = data.replace('\t\t','\t')
data = [i.strip().replace('\t',' ').split(' ') for i in data.strip().split('\n')]
sleep(3)
main(data)
mainloop_time = time() - starting_time - setup_time
print(f"Took {setup_time}s to setup, "
      f"{mainloop_time}s for mainloop.")
