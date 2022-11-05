import os
from sys import argv, exit
from configparser import ConfigParser


def main(fname):
    cfg = ConfigParser()
    cfg.read(os.path.expanduser("~")+"/.uzoenr/bm.ini")
    speak = cfg["Speech"]["app"]
    os.system(f"cat ~/.uzoenr/library/{fname} | {speak}")

def start():
    try:
        fnamo = argv[1]
        app = argv[0]
        main(fnamo)
    except IndexError:
        print("Запуск синтезатора речи:")
        print("Использование:")
        print('gruzau-speak: имя-файла')
    except FileNotFoundError:
        print(f"{fnamo}: Файл не найден")

if __name__ == '__main__':
    start()
