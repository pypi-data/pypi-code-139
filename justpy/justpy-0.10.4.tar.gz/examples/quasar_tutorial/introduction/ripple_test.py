# Justpy Tutorial demo ripple_test from docs/quasar_tutorial/introduction.md
import justpy as jp
# https://quasar.dev/vue-directives/material-ripple#Ripple-API

def ripple_test():
    wp = jp.QuasarPage()
    d = jp.QDiv(classes="q-pa-md q-gutter-md row justify-center", a=wp)
    d1 = jp.QDiv(v_ripple={'center': True, 'color': 'orange-5'}, classes="relative-position container bg-grey-3 text-black inline flex flex-center", text='center',
                 style='border-radius: 50%; cursor: pointer; width: 150px; height: 150px', a=d)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("ripple_test",ripple_test)
