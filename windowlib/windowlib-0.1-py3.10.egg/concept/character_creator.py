#!/usr/bin/env python3

### Character Creator: A curses based D&D Character Creator, based only on
### what I remember from when I was 14. Enjoy.

import json
import sys
import time

sys.path.insert(1, "/home/james/PycharmProjects/FramedWindow/")
from window import *

attributes = {
    "form_labels": [
        "Name",
        "Class",
        "Alignment",
        "Sex",
        "Race",
        "Strength",
        "Dexterity",
        "Constitution",
        "Intelligence",
        "Wisdom",
        "Charisma"
    ],
    "sheet_codes": [
        "NAME",
        "CLASS",
        "ALN",
        "SEX",
        "RACE",
        "STR",
        "DEX",
        "CON",
        "INT",
        "WIS",
        "CHR"
    ],
    "values": [
    ]
}



def create_chatacter():
    # start window
    window = DefaultWindow()
    # start form, for a questionaire style input group
    inputs = Form()
    # SCREEN #1
    # Run the form, with a list of labels
    inputs.run_form(*attributes["form_labels"])
    window.recompile_window()

    ## SCREEN #2 
    # print the character sheet 
    charname = inputs.responses[0]
    end = inputs.responses.pop()
    # Width: 132 - default 6 characters spacging between the buttons, so 40 + 40 + 40 + 6 + 6
    Button(" --- [ {} ] ---".format(charname), width=132, centered=True, style="cyan")
    for x, resp in enumerate(inputs.responses):
        if x == 0: continue
        attributes["values"].append(resp)
        if x % 3 == 0:
            Button(attributes["sheet_codes"][x] + ": " + str(resp), width=40)
        else:
            Button(attributes["sheet_codes"][x] + ": " + str(resp), width=40, reset_xpos=False)
    
    Button("Warning: You need to go outside more!", width=60, style="red")
    
    ## Wanna write it to JSON?
    save_menu = Menu()
    save_menu.register_button(Button("Save Character", width=20, style="green"))
    save_menu.register_button(Button("Destroy Character", width=20, style="red"))
    
    ans = save_menu.run_menu()

    if ans == 0:
        with open("characters/" + charname, "w") as dump_fb:
            
            json.dump(attributes, dump_fb, indent=4, sort_keys=False)
            window.cprint("Wrote to {}! ".format(charname), style="cyan")
    time.sleep(1)



if __name__ == "__main__":
    create_chatacter()
