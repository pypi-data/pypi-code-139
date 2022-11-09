from . import liuyuanlin
import sys

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        if("T" in sys.argv[1].upper() or "TELL"in sys.argv[1].upper()):
            print("没写")
    else:
        print("lll")
        liuyuanlin()