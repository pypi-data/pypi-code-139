import betterTUI

def custom_exit(screen, child_obj):
    exit()

def home(screen, child_obj):

    max_y, max_x = screen.getmaxyx()

    quit_button = (betterTUI.Button(screen, 2, 3, "Quit"), custom_exit)
    search_bar = (betterTUI.SearchBar(screen, int(max_x/2-15), 2, 30, "Search Song:", "Go"), custom_exit)

    # navbar line
    betterTUI.Line(screen, 0, 6, '─')

    # side info line
    betterTUI.Line(screen, 10, 3, '│', 0, True)

    screen.box()
    elements = [[quit_button, search_bar]]
    return elements