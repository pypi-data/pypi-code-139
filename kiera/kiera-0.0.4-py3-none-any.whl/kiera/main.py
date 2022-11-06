#!/usr/bin/env python3

import requests
import argparse
import random
import time
import tomli
import tomli_w
import os
import sys

from rich.columns import Columns
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner, SPINNERS

from rich.console import Console
console = Console()

SERVER_URL_DEV = 'http://localhost:5000'
SERVER_URL_PROD = 'https://jkl-backend-eu.herokuapp.com'

if sys.argv[1] == '--dev':
    SERVER_URL = SERVER_URL_DEV
    sys.argv.pop(1)
else:
    SERVER_URL = SERVER_URL_PROD

TERMS_AND_SEVICES = 'https://jkl2.vercel.app/'

CLIENT_ID="6ba695f9a731779de3eb"

STATE = str(random.random())

CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'kierarc')

def write_access_key_to_file(access_key):
    data = {'access_key': access_key}
    with open(API_KEYS_LOCATION, 'w') as f:
        f.write(tomli_w.dumps(data))

def read_access_key_from_file():
    if not os.path.exists(API_KEYS_LOCATION):
        return None

    with open(API_KEYS_LOCATION, 'r') as f:
        data = tomli.loads(f.read())

    if 'access_key' not in data:
        return None

    return data['access_key']

ACCESS_KEY = read_access_key_from_file()

def server_test():
    r = requests.get(f'{SERVER_URL}/test')
    print(r.text)

def hello():
    print("Hello, world!")
    print('Trying to connect to the server...')
    server_test()


def login():
    accepted_tns = terms_and_sevices_prompt()
    if not accepted_tns:
        return
    url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&state={STATE}'
    # print(url)
    print(f'In case your browser doesn\'t open automatically, visit \n{url}')
    webbrowser.open(url)
    while True:  
        access_key = get_access_key_from_state(STATE)
        if access_key:
            print('Access key received')
            break
        time.sleep(0.5)

    write_access_key_to_file(access_key)
    return access_key



def terms_and_sevices_prompt():
    print(f'Terms and Services: {TERMS_AND_SEVICES}')
    print('Do you agree to the terms and services? [y/n]')
    answer = input()
    if answer == 'y':
        return True
    else:
        return False

def listen_for_callback():
    print('Listening for callback', flush=True)
    import flask
    app = flask.Flask(__name__)

    @app.route('/github/callback', methods=['GET'])
    def callback():
        print('Callback received')
        print(flask.request.args)
        return 'You can close this window now'

    # app.run()
    app.run(host='localhost', port=5000, debug=True)

def parse_args():
    parser = argparse.ArgumentParser(description='Kiera')
    # parser.add_argument('command', choices=['login', 'listen'])
    # parser.add_argument('command', choices=['login', ''])
    # parser.add_argument('login', action='store_true')
    # make login command optional
    parser.add_argument('command', nargs='?', choices=['login', ''])
    return parser.parse_args()

def main():
    # args = parse_args()
    # if args.login:
        # login()
        # listen_for_callback()
    # else:
        # hello()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'login':
            arg_login = True
        else:
            arg_login = False


    if not ACCESS_KEY:
        print('No access key found, running login')
        # args.command = 'login'
        arg_login = True

    # if args.command == 'login':
    if arg_login:
        login()
        # listen_for_callback()
    else:
        # hello()
        generate_completion()
        if False:
            input_text = '# test:'
            r = requests.post(SERVER_URL + '/main2', json={'data': input_text, 'access_key': access_key})
            print("r:", r)
            print(r.text)

def generate_completion():
    input_text = ' '.join(sys.argv[1:])
    while True:
        with console.status('', spinner='aesthetic'):
            # r = requests.post(SERVER_URL, data={'data': input_text})
            r = requests.post(SERVER_URL + '/main2', json={'data': input_text, 'access_key': ACCESS_KEY})


        parsed = r.json()
        data = parsed['data']

        import subprocess as sp

        def execute_command(command):
            sp.run(command, shell=True)


        import colored

        print(f'{data}     Execute (Y/n)?', end='\r')

        sys.stdout.flush()

        import getch
        execute_answer = getch.getch().strip()

        if execute_answer in ['y', 'Y', '']:
            print()
            execute_command(data)
            break







def get_access_key_from_state(state):
    response = requests.post(f'{SERVER_URL}/get_access_key_from_state', json={'state': state})
    print(response.text)
    access_key = response.json()['jkl_access_key']
    return access_key


import webbrowser

if __name__ == "__main__":
    # webbrowser.open('http://example.com') 
    # get_access_key_from_state('0.6621392675885354')
    main()


    # hello()
    # login()
    # r = requests.post(SERVER_URL + '/main', data={'data': input_text})
    # as application/json
    if False:
        input_text = '# print all files'
        r = requests.post(SERVER_URL + '/main', json={'data': input_text})
        print("r:", r)
        print("r.text:", r.text)

