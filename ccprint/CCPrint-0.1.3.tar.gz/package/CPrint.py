class CCPrint:
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

    def __init__(self):
        del self

    @classmethod
    def cprint(cls, *text, color='BLUE'):
        try:
            print(f'{cls.colors[str(color)]}' + ', '.join([str(t) for t in text]))
        except KeyError:
            print(f'{cls.colors["FAIL"]}KeyError: {color} not found! Available colors: {list(cls.colors.keys())}')
