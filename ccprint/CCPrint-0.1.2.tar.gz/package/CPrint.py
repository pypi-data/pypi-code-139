colors = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'CYAN': '\033[96m',
    'TRUE': '\033[92m',
    'WARNING': '\033[93m',
    'FALSE': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m'
}


def cprint(*text, color='OKBLUE'):
    try:
        print(f'{colors[str(color)]}' + ', '.join([str(t) for t in text]))
    except KeyError:
        print(f'{colors["FAIL"]}KeyError: {color} not found! Available colors: {list(colors.keys())}')
