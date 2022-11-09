from textwrap import wrap
from . import animals
from .util import animalsay, INDENT_DEFAULT, MAXWIDTH_DEFAULT


def cowsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.COW, indent=indent)

def pigsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.PIG, indent=indent)

def chickensay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.CHICKEN, indent=indent)

def sheepsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.SHEEP, indent=indent)

def penguinsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.PENGUIN, indent=indent)

def dogsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return animalsay(wrap(message, maxwidth), animal=animals.DOG, indent=indent)

def farmsay(message, maxwidth=MAXWIDTH_DEFAULT, indent=INDENT_DEFAULT):
    return (animalsay(wrap(message, maxwidth), animal=animals.COW, indent=indent) 
    + "\n" + animalsay(wrap(message, maxwidth), animal=animals.PIG, indent=indent)
    + "\n" + animalsay(wrap(message, maxwidth), animal=animals.CHICKEN, indent=indent)
    + "\n" + animalsay(wrap(message, maxwidth), animal=animals.SHEEP, indent=indent)
    +"\n" + animalsay(wrap(message, maxwidth), animal=animals.PENGUIN, indent=indent)
    + "\n" + animalsay(wrap(message, maxwidth), animal=animals.DOG, indent=indent))
