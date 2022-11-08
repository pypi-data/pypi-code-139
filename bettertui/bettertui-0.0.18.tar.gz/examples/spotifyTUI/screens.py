import betterTUI
import globals
from datetime import datetime

def custom_exit(screen, child_obj):
    exit()

def getTime():
    now = datetime.now()
    return f"Current Time: {now.strftime('%H:%M:%S')}"

def home(screen, child_obj):

    max_y, max_x = screen.getmaxyx()

    quit_button = (betterTUI.Button(screen, 2, 3, "Quit"), custom_exit)
    search_bar = (betterTUI.SearchBar(screen, int(max_x/2-15), 2, 30, "Search Song:", "Go"), custom_exit)

    # navbar line
    betterTUI.Line(screen, 0, 6, '─')

    # side info line
    betterTUI.Line(screen, int(max_x/4), 3, '│', 0, True)

    # box screen
    screen.box()

    # intersection chars
    betterTUI.Text(screen, int(max_x/4), 6, "┬")
    betterTUI.Text(screen, int(max_x/4), max_y-1, "┴")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # real time updated hours:minutes:seconds
    text = betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(f"Current Time: {current_time}")/2), max_y-4, f"Current Time: {current_time}")

    text.real_time_update(1, getTime)

    # show current song
    if('title' in globals.song):
        pass
    else:
        # Song Title
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len("Currently Playing:")/2), 10, "Currently Playing:")
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len("None")/2), 11, "None")

        # Song timeleft
        betterTUI.Text(screen, int(max_x/4-(max_x/4)/2-len(f"{'─'*10} 00:00")/2), 13, f"{'─'*10} 00:00")

    trash = [text]
    elements = [[quit_button, search_bar]]
    return { 'elements': elements, 'trash': trash }