import sys
from . import pyfarmsay


def main():
    if len(sys.argv) > 1:
        animal = sys.argv[1].lower()
        message = " ".join(sys.argv[2:])
        return call_animal(animal, message)
    else:
        return "You have to specify the pyanimal in the pyfarm that you would like to see."
  
def call_animal(animal, message):
    if animal == "cow":
       return pyfarmsay.cowsay(message)
    elif animal == "pig":
        return pyfarmsay.pigsay(message)
    elif animal == "chicken":
        return pyfarmsay.chickensay(message)
    elif animal == "dog":
        return pyfarmsay.dogsay(message)
    elif animal == "penguin":
        return pyfarmsay.penguinsay(message)
    elif animal == "sheep":
        return pyfarmsay.sheepsay(message)
    elif animal == "farm":
        return pyfarmsay.farmsay(message)
    else:
        return "animal not in farm :(!"

if __name__ == "__main__":
    print(main())



