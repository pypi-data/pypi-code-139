from betterTUI import *
from screens import *
import globals, sys
globals.initialize()

def main(screen):
    global wrapper
    
    curses.curs_set(0)

    state = home(screen, None)

    while(True):

        wrapper = Wrapper(screen, [0,0], state['elements'], state['trash'])
        res = wrapper.on('ALT_Q')

        screen.clear()
        wrapper.delete()

        if(res in ['ALT_Q']): break
        else: state = res[1](screen, res[0])

try:
    Screen(main)
except (KeyboardInterrupt, SystemExit):
    wrapper.delete()
    sys.exit()