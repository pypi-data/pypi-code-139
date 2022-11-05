import os
import sys
import atexit
from Colors import Colors

os.system('')

# THIS FUCNTION IS USED TO CLEAR THE SCREEN EVERY TIME THE PROGRAM HAS EXITED.
def exit_handler():

    if Terminal.Exit_Mode:
        sys.stdout.write(Terminal.End)
        Terminal.Cursor.Clear()

atexit.register(exit_handler)


# THIS CLASS IS USED TO CONTROL VARIOUS PARAMETERS LIKE COLOR CURSOR AND FONTS
class Terminal:

    ### mode con:cols=80 lines=100 ### from windows screen

    Main_Win_Bg_Color = '\x00'
    Main_Txt_Bg_Color = '\x00'
    Main_Txt_Fr_Color = '\x00'

    Null = '\x00'
    End = f'\x1b[0m'
    SYS_Reset = '\x1b[!p'

    Exit_Mode=False

    Verbose = True
    Title = lambda title: sys.stdout.write(f'\x1b]0;{title}\x07')
    Prefix = lambda  : sys.stdout.write(Terminal.End+Terminal.Main_Win_Bg_Color)

    BG_array = []
    FR_array = []

    format = Main_Win_Bg_Color + \
             Main_Txt_Bg_Color + \
             Main_Txt_Fr_Color

    class Cursor:

        Save = lambda : sys.stdout.write(f'\x1b[s')
        Restore = lambda : sys.stdout.write( f'\x1b[u')
        Del = lambda line: f'\x1b[{line}M'


        Clear = lambda : sys.stdout.write(f'\x1b[2J')
        Hide  = lambda : sys.stdout.write(f'\x1b[?25l')
        Show  = lambda : sys.stdout.write(f'\x1b[?25h')
        Origin = lambda: sys.stdout.write(f'\x1b[H')

        class Shape:

            # Cursor_Shape  # 'ESC[<n> q'
            Default = lambda : sys.stdout.write('\033[0 q')
            Binking_block = lambda : sys.stdout.write( '\033[1 q')
            Steady_block = lambda : sys.stdout.write( '\033[2 q')
            Blinking_underline = lambda : sys.stdout.write( '\033[3 q')
            Steady_underline = lambda : sys.stdout.write( '\033[4 q')
            Blinking_bar = lambda : sys.stdout.write('\033[5 q')
            Steady_bar = lambda : sys.stdout.write('\033[6 q')

        class Move:  # SYS_COMMNDS

            Up       = lambda line=0: sys.stdout.write(f'\033[{line}A')
            Down     = lambda line=0: sys.stdout.write(f'\033[{line}B')
            Forward  = lambda line=0: sys.stdout.write(f'\033[{line}C')
            Backward = lambda line=0: sys.stdout.write(f'\033[{line}D')
            Nxt_Line = lambda line=0: sys.stdout.write(f'\033[{line}E')
            Pre_Line = lambda line=0: sys.stdout.write(f'\033[{line}f')
            Position = lambda line=0, column=0: sys.stdout.write(f'\033[{line};{column}H')

            Scroll_Up   = lambda line=1: Terminal.write(f'\x1b[{int(line)}T')
            Scroll_Down = lambda line=1: Terminal.write(f'\x1b[{int(line)}S')

    class Text:

        # Decorations
        Bold = '\x1b[1m'
        Italic = '\x1b[3m'
        Underline = '\x1b[4m'
        Blink = '\x1b[5m'

        Swap = lambda: sys.stdout.write('\x1b[7m')  # \x1b[0m

    class Font:

        m_L ='\x1b(0\x6a\x1b(B'        # ┘
        fm_L ='\x1b(0\x6b\x1b(B'       # ┐
        f_L ='\x1b(0\x6c\x1b(B'        # ┌
        L ='\x1b(0\x6d\x1b(B'          # └
        x ='\x1b(0\x6e\x1b(B'          # ┼
        __ ='\x1b(0\x71\x1b(B'         # ─
        le_T ='\x1b(0\x74\x1b(B'       # ├
        ri_T ='\x1b(0\x75\x1b(B'       # ┤
        re_T ='\x1b(0\x76\x1b(B'       # ┴
        T ='\x1b(0\x77\x1b(B'          # ┬
        line ='\x1b(0\x78\x1b(B'       # │

    @staticmethod  # NOT FOR USER
    def Error(error=Null, name=Null,exit_=False):

        if Terminal.Verbose:
            Th = Colors.BG_Black + Colors.FR_Red + Terminal.Text.Underline
            err = f"{Th}: {name} : Error : {error} :{Terminal.End}{Terminal.Main_Win_Bg_Color}"
            Terminal.write(err)

            if exit_:
                Terminal.Exit_Mode=False
                exit()

    @staticmethod  # NOT FOR USER
    def Message(message=Null, name=Null):
        if Terminal.Verbose:
            Th = Colors.BG_Black + Colors.FR_B_Green +  Terminal.Text.Underline
            msg = f"{Th}: {name} : Message : {message} :{Terminal.End}{Terminal.Main_Win_Bg_Color}"
            Terminal.write(msg)

    @staticmethod
    def Reset():

        Terminal.Main_Bg_Color='\x00'
        Terminal.Main_Fr_Color='\x00'
        Terminal.Cursor.Shape.Default()
        sys.stdout.write('\x1b[0m')
        os.system('cls') #REMEBER TO CORRECT
        Terminal.Message(message=f"Terminal Reset Done",name="Terminal")

    @staticmethod #improve this method by reducing num of opreation
    def Show_Colors(show=True):

        x = vars(Colors)
        ignore_keys = ['__module__', 'Main_Bg_Color', 'Main_Fr_Color', 'Swap', '__dict__', '__weakref__', '__doc__']
        keys = []
        for i in x:
            if i not in ignore_keys:
                keys.append(i)

        if len(Terminal.BG_array) == 0 and len(Terminal.FR_array) == 0:
            for i in keys:
                if "BG" in i:
                    Terminal.BG_array.append(x[i])
                elif "FR" in i:
                    Terminal.FR_array.append(x[i])
        if show:
            Terminal.Message(message="All this Colors can can be used by their respected attribute", name="Show_Colors")
            for i in keys:
                print(f"Terminal.Colors.{i} = " + x[i] + "+----+" + Terminal.End)

    @staticmethod #LINUX ADDKARVA NU CHE AJU
    def Set_Window_Bg_Color(color):

        x = color.replace("\x1b[", " ")
        x = x.replace("m", " ")
        if int(x) in list(range(40, 48)) + list(range(100, 108)):
            sys.stdout.write(color)
            Terminal.Main_Win_Bg_Color = color

        if os.name == 'nt':
            Terminal.Cursor.Clear()
            Terminal.Message(message=f"Terminal Background Color Set to {color}||||",name="Set_terminal_color")
        elif os.name == "posix":
            os.system('clear')
            Terminal.Message(message=f"Terminal Background Color Set to {color}||||", name="Set_terminal_color")

        else:
            Terminal.Error(error=f"Enter A valid color which has word 'BG' in it .", name="Set_Window_Bg_Color")

    @staticmethod
    def Set_Text_Bg_Color(color):
        x=color.replace("\x1b[", " ")
        x=x.replace("m"," ")
        if int(x) in list( range(40,48)) + list(range(100,108)):
            Terminal.Main_Txt_Bg_Color=color
            Terminal.Message(message=f"Text BG color Set to {Terminal.Main_Txt_Bg_Color}||||",name="Set_Text_Bg_Color")
        else:
            Terminal.Error(error=f"Enter A valid color which has word 'BG' in it .",name="Set_Text_Bg_Color")

    @staticmethod
    def Set_Text_Fr_Color(color):
        x = color.replace("\x1b[", " ")
        x = x.replace("m", " ")
        if int(x) in list(range(30, 38)) + list(range(90, 98)):
            Terminal.Main_Txt_Fr_Color = color
            Terminal.Message(message=f"Text FR color Set to {Terminal.Main_Txt_Fr_Color}||||{Terminal.End}", name="Set_Text_Fr_Color")
        else:
            Terminal.Error(error=f"Enter A valid color which has word 'FR' in it .", name="Set_Text_Fr_Color")

    @staticmethod
    def write(string="",new_line=True,theme='\x00'):

        if new_line:
            sys.stdout.write(f'{Terminal.format}{theme}{string}{Terminal.End}{Terminal.Main_Win_Bg_Color}\n')
            sys.stdout.flush()

        else:
            sys.stdout.write(f'{Terminal.format}{theme}{string}{Terminal.End}{Terminal.Main_Win_Bg_Color}')
            sys.stdout.flush()