import os
import sys
import cv2
import pathlib
import numpy as np
from PIL import Image
from time import sleep
from Terminal import Terminal

# THIS IS A SUPPORTING SYSTEM CLASS
class Main:

    Mode = "print"
    Out_File = None
    Default_Ext = ".aplay"

    Allowed_VF = ['.mp4', '.mkv']
    Allowed_IF = ['.jpg', '.png', '.jpeg','.bmp']

    Video_File = False
    Write_Header = False
    Save_location="Aplay/Saved/"

    MoreLevels = True
    Camera_Gscale = False

    # 70 levels of gray
    gscale1 = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    # 10 levels of gray
    gscale2 = r'@%#*+=-:. '
    # 21 levels of gray for cam
    gscale3 = r"?-_+~<>i!lI;:,\"^`'. "

# THIS CLASS IS USED TO PLAY VIDEOS AND IMAGES INTO ASCII.
class Ascii_Display:

    @staticmethod
    def convert(img):

        if Main.Video_File:
            image = Image.fromarray(img).convert('L')
        else:
            image = Image.open(img).convert('L')

        W, H = image.size
        cols = 150
        scale = 0.43
        w = W / cols
        h = w / scale
        rows = int(H / h)

        if cols > W or rows > H:
            print("")
            Terminal.Error(error="Image too small for specified cols!",name="Ascii_Display.convert",exit_=True)

        def getAverageL(image):

            im = np.array(image)
            w, h = im.shape
            return np.average(im.reshape(w * h))

        aimg = []
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            if j == rows - 1:
                y2 = H
            aimg.append("")

            for i in range(cols):
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                if i == cols - 1:
                    x2 = W
                img = image.crop((x1, y1, x2, y2))
                avg = int(getAverageL(img))

                if Main.MoreLevels:
                    gsval = Main.gscale1[int((avg * 69) / 255)]
                elif Main.Camera_Gscale:
                    gsval = Main.gscale3[int((avg * len(Main.gscale3) - 1) / 255)]
                else:
                    gsval = Main.gscale2[int((avg * 9) / 255)]

                aimg[j] += gsval

        if Main.Mode == "print":
            Terminal.write('\x1b[H', new_line=False)
            for row in aimg:
                Terminal.write(f"{row}\n", new_line=False)
            # Terminal.write('\b', new_line=False)

        elif Main.Mode == "save":

            if Main.Write_Header:
                with open(Main.Out_File, 'w') as file:
                    file.write(f"row{rows}:col{cols}:scale{scale}\n")
                    Main.Write_Header = False

            with open(Main.Out_File, "a") as file:
                file.write('\x1b[H')
                for row in aimg:
                    file.write(f"{row}\n")

    # Function to extract frames
    @staticmethod
    def Video_(vid):

        Main.Video_File=True

        vidObj = cv2.VideoCapture(vid)
        total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))

        for i in range(int(total_frames)):
            vidObj.set(cv2.CAP_PROP_POS_FRAMES, i)
            success, frame = vidObj.read()
            if success:
                Ascii_Display.convert(img=frame)
                Main.Write_Header = False

        Main.Video_File = False

    @staticmethod
    def Camera_():

        Terminal.Cursor.Move.Position(line=49,column=170)
        Terminal.write(": Press 'q' to stop :")

        vidObj = cv2.VideoCapture(0)

        success = 1
        while success:
            success, frame = vidObj.read()
            if success:
                Ascii_Display.convert(img=frame)
                Main.Write_Header = False

                key = cv2.waitKey(1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        Main.Video_File = False
        Main.MoreLevels = True

    @staticmethod
    def Play(file, speed=0.05):

        if os.path.isfile(file) and (file).split('.')[-1] == "aplay":
            with open(file, 'r') as file:
                x = file.readlines()
                header = x[0]
                rows = int(header.split(':')[0].replace('row', ''))
        else:
            Terminal.Error(error=f"The given soruce '{file}' is Invalid or it's not supproted format.",
                           name="Ascii_Display.Play")
        last_row = 1
        row = rows
        for i in range(int(len(x) / rows)):
            strx = x[last_row:row]
            strx = ' '.join(strx)
            Terminal.write(string=f"{strx}", new_line=False)
            last_row = row
            row += rows
            sleep(speed)

    @staticmethod
    def Media(soruce, mode="print"):

        if mode is not None and type(mode) == str and mode in ["print", "save"]:
            Main.Mode = mode
            if Main.Mode == "save":
                Main.Write_Header=True
                Main.Out_File = f"{os.path.basename(soruce).split('/')[-1].split('.')[0]}{Main.Default_Ext}"
        else:
            Terminal.Error(error=f"Mode {mode} is Invalid. Using Default mode 'print'", name="img2ascii.Play",
                           exit_=True)

        if type(soruce) is str:

            if soruce == "camera":
                Main.Video_File = True
                Ascii_Display.Camera_()

            elif os.path.isfile(soruce):
                if pathlib.Path(soruce).suffix.lower() in Main.Allowed_IF:
                    Ascii_Display.convert(img=soruce)

                elif pathlib.Path(soruce).suffix.lower() in Main.Allowed_VF:
                    Main.Video_File=True
                    Ascii_Display.Video_(vid=soruce)
        else:
            Terminal.Error(error=f"The given soruce '{soruce}' is Invalid or it's not supproted format.",
                           name="Ascii_Display.Play", exit_=True)