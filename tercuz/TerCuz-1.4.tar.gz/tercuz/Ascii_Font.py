import os
import pyfiglet
from time import sleep
from Terminal import Terminal


# THIS CLASS IS USED TO WRITE TEXT IN ASCII FONTS
class Ascii_Font:

    Font_array = None
    _Last_Font_ = None
    _Font_ = None
    status=True

    @staticmethod  # NOT FOR USER
    def List_fonts():

        if Ascii_Font.Font_array is None:

            mod_path = pyfiglet.__file__.replace("__init__.py", "fonts")
            fonts = os.listdir(mod_path)

            fonts = [f for f in fonts if f.endswith('.flf') or f.endswith('.flc')]
            fonts = [f.replace('.flf', '') for f in fonts]
            fonts = [f.replace('.flc', '') for f in fonts]

            Ascii_Font.Font_array = fonts
            return Ascii_Font.Font_array

        else:
            return Ascii_Font.Font_array

    @staticmethod
    def Show_fonts():
        name = Ascii_Font.Show_fonts.__name__
        if Ascii_Font.Font_array is not None:

            num = 1
            for i in Ascii_Font.Font_array:
                print(f"{num} : {i}\n")
                try:
                    print(pyfiglet.figlet_format(f"{i}", font=i))
                    sleep(0.25)
                except pyfiglet.FontNotFound:
                    Terminal.Error(error="Sorry Unable to load This font !!! (File might be missing or corrupted) ",
                                   name=name)
                    sleep(0.50)
                num += 1
        else:
            Ascii_Font.Font_array = Ascii_Font.List_fonts()
            Ascii_Font.Show_fonts()

    @staticmethod  # NOT FOR USER
    def chk_font(font):
        name = Ascii_Font.chk_font.__name__
        try:
            pyfiglet.figlet_format("FONT", font=font)
            return True
        except pyfiglet.FontNotFound:

            Terminal.Error(error="Sorry Unable to load This font !!! (File might be missing or corrupted", name=name)
            return False

    @staticmethod
    def Set_Font(val):

        name = Ascii_Font.Set_Font.__name__
        if Ascii_Font.Font_array is not None:

            if type(val) is int:
                if val > len(Ascii_Font.Font_array):
                    Terminal.Error(error=f"Select from range 0 to {len(Ascii_Font.Font_array)}", name=name)
                else:
                    if Ascii_Font.chk_font(Ascii_Font.Font_array[val]):
                        Ascii_Font._Last_Font_ = Ascii_Font._Font_
                        Ascii_Font._Font_ = Ascii_Font.Font_array[val]
                        Ascii_Font.status = True

                        Terminal.Message(message=f"Font Set to {Ascii_Font.Font_array[val]}", name=name)

            elif type(val) is str:

                if val in Ascii_Font.Font_array:

                    if Ascii_Font.chk_font(val):
                        Ascii_Font._Last_Font_ = Ascii_Font._Font_
                        Ascii_Font._Font_ = val
                        Ascii_Font.status = True
                        Terminal.Message(message=f"Font Set to {val}", name=name)

                elif val == "off":
                    Ascii_Font.status = False
                    Terminal.Message(message=f"Font {Ascii_Font._Font_} Set to Off", name=name)

                elif val is None and Ascii_Font._Last_Font_ is None:
                    Ascii_Font._Last_Font_ = Ascii_Font._Font_
                    Ascii_Font._Font_ = val
                    Ascii_Font.status = True
                    Terminal.Message(message=f"Font Set to {val}", name=name)

                else:
                    Terminal.Error(error=f"Unable to find font {val} ", name=name)

            elif val == Ascii_Font._Last_Font_:
                if val is None:
                    Ascii_Font._Font_ = val
                    Ascii_Font.status = False
                    Terminal.Message(message=f"Font Set to {val} and Art mode is off", name=name)
                else:
                    Ascii_Font._Font_ = val
                    Terminal.Message(message=f"Font Set to {val}", name=name)
            else:
                Terminal.Error(error=f"Unable to find font {val} ", name=name)

        else:
            Ascii_Font.Font_array = Ascii_Font.List_fonts()
            Ascii_Font.Set_Font(val)

    @staticmethod
    def write(string,new_line=True,theme='\x00'):

        string=string.upper()

        if Ascii_Font.status and Ascii_Font._Font_ is not None:
            string = pyfiglet.figlet_format(f"{string}", font=Ascii_Font._Font_)
            Terminal.write(string, new_line=new_line,theme=theme)

        else:
            Terminal.Error(error="Oops! You called Ascii_Font class but no font has been selected or status is false",name="Ascii_Font.write")