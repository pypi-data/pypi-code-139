import sys
from Terminal import Terminal
from Ascii_Font import Ascii_Font
from Colors import Colors
from time import sleep
import random

# THIS CLASS IS USED TO PERFORM ANIMATION ON A GIVEN TEXT STRING.
class Animations:

    Loop = False
    Speed = 0.25
    Override = False
    ascii_fonts = True  #marck we need to add this method to enable ascii fonts in animations

    @staticmethod
    def Fall(string, speed=Speed, loop=Loop, font=None,theme=Colors.BG_Black+Colors.FR_Yellow):

        if font is not None and Ascii_Font.status:
            Ascii_Font.Set_Font(font)
            class_=Ascii_Font
        else:
            class_=Terminal


        x = ([*string])
        Terminal.Cursor.Hide()

        for i in x:
            class_.write(string=i, new_line=True,theme=theme)
            sleep(speed)

        Terminal.Cursor.Show()
        sys.stdout.write('\n')

        if loop or Animations.Loop:
            while True:
                Animations.Fall(string=x)

    @staticmethod
    def Play(string, speed=0.35, loop=Loop, font=None,theme=Colors.BG_Red+Colors.FR_Yellow):

        if font is not None and Ascii_Font.status:
            Ascii_Font.Set_Font(font)
            class_=Ascii_Font
        else:
            class_=Terminal

        x = ([*string])
        for i in x:
            Terminal.Cursor.Save()
            class_.write(string=i, new_line=False,theme=theme)
            Terminal.Cursor.Restore()
            sleep(speed)

        Terminal.Cursor.Restore()
        class_.write(string="    ", new_line=True,theme=theme)

        Terminal.Cursor.Show()
        Ascii_Font.Set_Font(Ascii_Font._Last_Font_)

        if loop or Animations.Loop:
            while True:
                Animations.Play(string=x)

    @staticmethod
    def Erase_Line(string, speed=Speed, loop=Loop, replace=" ", move="<"):

        x = ([*string])
        Terminal.Cursor.Hide()
        if move == "<":
            Terminal.write(string, new_line=False)
            num = 1
            for i in x:
                sleep(speed)
                Terminal.Cursor.Move.Backward(num)
                Terminal.write(replace, new_line=False)
                num = 2
            Terminal.Cursor.Show()

        elif move == ">":

            num = len(x)
            Terminal.Cursor.Move.Backward(num)
            Terminal.write(string, new_line=False)
            Terminal.Cursor.Move.Backward(num)
            for i in x:
                sleep(speed)
                Terminal.Cursor.Move.Forward(1)
                Terminal.Cursor.Move.Backward(1)
                Terminal.write(replace)
            Terminal.Cursor.Show()

        else:
            Terminal.Error(error="Invalid move detected parameter move can be either '<' or '>'",
                           name="Animations.Erase_Line")
            return None

        if loop or Animations.Loop:
            while True:
                Animations.Erase_Line(string=string, move=move, replace=replace)

    @staticmethod
    def Blink(string,font=None,times=0, speed=0.10, loop=Loop, override=False):

        Terminal.write()
        x = ([*string])
        if override:
            string = string
        else:
            string = Colors.BG_Black + Colors.FR_B_Green + string + Terminal.End

        if times != 0:
            if times > 50:
                time = 50
                Terminal.Error(
                    error=f": Times has benn set to Max {str(time)} : Invalid Time Value Detected. Input must be >= 50)",
                    name="Animations.Blink")
            elif times < 5:
                time = 5
                Terminal.Error(
                    error=f": Times has been set to Min {str(time)} : Invalid Time Value Detected. Input must be >= 5)",
                    name="Animations.Blink")
            else:
                time = times
        else:
            time = int(len(string) / 2)
            Terminal.Error(
                error=f": Time has been set to Default {str(time)} : Invalid Time Value Detected. Note times value "
                      "should be int only. (preferred value greater than 5 and smaller than 50 )",
                name="Animations.Blink")

        Terminal.Cursor.Save()
        Terminal.Cursor.Hide()
        for i in range(1, time):
            Terminal.write(string, new_line=False)
            sleep(speed)
            Terminal.Cursor.Restore()
            Terminal.write(Colors.BG_Black + " " * (len(x)), new_line=False)
            Terminal.Cursor.Restore()
            sleep(speed)

        Terminal.Cursor.Show()
        if loop or Animations.Loop:
            while True:
                Animations.Blink(string=string, speed=speed)

    @staticmethod
    def Slide_Colors(string, font=None,loop=Loop):

        if font is not None and Ascii_Font.status:
            Ascii_Font.Set_Font(font)
            class_=Ascii_Font
        else:
            class_=Terminal

        Terminal.write()
        speed = 0.0001
        Terminal.Show_Colors(show=False)
        Terminal.Cursor.Hide()
        x = ([*string])

        Terminal.Cursor.Save()
        Terminal.write(string, new_line=False)
        Terminal.Cursor.Restore()
        num = 0
        for txt_color in Terminal.FR_array:

            z = txt_color.replace("\x1b[", "")
            z = z.replace("m", "")
            if int(z) in [30, 37, 90, 97]:
                continue
            for i in x:
                sleep(speed)
                Terminal.Cursor.Move.Forward(1)
                Terminal.Cursor.Move.Backward(1)
                Terminal.write(i, new_line=False,theme=Colors.BG_Black + txt_color)

            Terminal.Cursor.Restore()
        Terminal.Cursor.Show()

        if loop or Animations.Loop:
            while True:
                Animations.Slide_Colors(string=string)

    @staticmethod
    def Random_Colors(string, font=None, speed=0.10, loop=Loop):

        if font is not None and Ascii_Font.status:
            Ascii_Font.Set_Font(font)
            class_ = Ascii_Font
        else:
            class_ = Terminal

        Terminal.Show_Colors(show=False)
        x = ([*string])

        Terminal.Cursor.Hide()
        Terminal.Cursor.Save()
        class_.write(string, new_line=False)
        Terminal.Cursor.Restore()

        for txt_color in Terminal.FR_array:
            z = txt_color.replace("\x1b[", "")
            z = z.replace("m", "")
            if int(z) in [30, 37, 90, 97]:
                continue
            sleep(speed)
            class_.write( string, new_line=False,theme=Colors.BG_Black + txt_color)
            Terminal.Cursor.Restore()
            Terminal.Cursor.Save()

        txt_color = random.choice(Terminal.FR_array)
        class_.write( string, new_line=False,theme=Colors.BG_Black + txt_color)
        Terminal.Cursor.Show()

        if loop or Animations.Loop:
            while True:
                Animations.Random_Colors(string=string)

    @staticmethod
    def Loading(message="Loading...", fill="_", replace="|", length=100, bar_color='\x1b[100m'):

        speed = 0.05
        Terminal.write()
        Terminal.Cursor.Hide()
        th = Colors.FR_B_Green + Terminal.Text.Underline

        if type(length) is int and length in range(20, 211):
            length = length
            Terminal.Message(message=f"Length set to Custom {length}",
                             name="Animations.Loading")
        else:
            length = 100
            Terminal.Error(error=f": Length set to Default {length} : Note length must be a int between 20 to 210 "
                           , name="Animations.Loading")

        if len(Terminal.BG_array) == 0:
            Terminal.Show_Colors(show=False)

        if bar_color in Terminal.BG_array:
            bar_color = bar_color
            Terminal.Message(message=f"bar_color set to Custom Background Color",
                             name="Animations.Loading")

        elif bar_color is None:
            if Terminal.Main_Txt_Bg_Color == '\x00':
                bar_color = Colors.BG_Black
                Terminal.Message(message="bar_color set to None", name="Animations.Loading")
            else:
                bar_color = Terminal.Main_Txt_Bg_Color
                Terminal.Message(message="bar_color set to None", name="Animations.Loading")

        else:
            Terminal.Error(
                error=f": Bar_Color set to Defalut : Please Select A valid Foreground_Color from Terminal.Colors.FR_*",
                name="Animations.Loading")
            bar_color = '\x1b[100m'

        if type(message) and type(replace) and type(fill) is not str:
            message = "Loading..."
            replace = "_"
            fill = "|"
            Terminal.Error(
                error=": Using Defaluts for message, replace, fill :Note values message, replace and fill should be string or any Ascii Value",
                name="Animations.Loading")
        else:
            message = message
            replace = replace
            fill = fill
            Terminal.Message(
                message=f" Values : Message='{message}', Replace='{replace}', Fill='{fill}' : Set Successfully",
                name="Animation.Loading")

        Terminal.write(th + message + '\n')
        Terminal.write(th + fill * length + Terminal.End, new_line=False)
        Terminal.Cursor.Move.Backward(length)
        Terminal.Cursor.Move.Backward(length)
        sleep(speed)
        for i in range(length):
            sleep(speed)
            Terminal.Cursor.Move.Forward(1)
            Terminal.Cursor.Move.Backward(1)
            Terminal.write(th + bar_color + replace, new_line=False)
        Terminal.Cursor.Show()