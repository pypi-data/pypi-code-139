import stern
def sumAB(a,b):
    return a - b
def SealN():
    n=5
    string="Hello beautiful world of programming!"
    print(string * n)
while True:
    print("1. Welcome")
    print("2. sum0391")
    print("3. SealN")
    print("0. Quit")
    cmd = input("Select an item: ")
    
    if cmd == "1":
        print("Welcome to the module Stern! Thank you for downloading this module!")
    elif cmd == "2":
        print(sumAB(2003, 1991))
    elif cmd == "3":
        SealN()
    elif cmd == "0":
        exit()
    else:
        print("You entered an invalid value")