from time import sleep


func_add = 0
func_sub = 0
func_mul = 0
func_div = 0
valid_operations = ["add", "Add", "addition", "Addition", "subtract", "Subtract", "subtraction", "Subtraction", "multiply", "Multiply", "multiplication", "Multiplication", "divide", "Divide", "square", "Square", "Divisibility", "divisibility", "power", "Power"]
operation_validator = 0
addition = 0
subtraction = 0
multiplication = 0
division = 0
square = 0
divisibility = 0
power = 0


def sahil():
    print("sahil is cool")

def  run_calc(operation):
    if operation == "add" or operation == "Add" or operation == "addition" or operation == "Addition":
        num1 = int(input("Enter the first number \n"))
        num2 = int(input("Enter the second number \n"))
        addition = num1 + num2
        print("The answer is:",addition)

    elif operation == "subtract" or operation == "Subtract" or operation == "subtraction" or operation == "Subtraction":
        num1 = int(input("Enter the first number \n"))
        num2 = int(input("Enter the second number \n"))
        subtraction = num1 - num2
        print("The answer is:",subtraction)

    elif operation == "multiply" or operation == "Multiply" or operation == "multiplication" or operation == "Multiplication":
        num1 = int(input("Enter the first number \n"))
        num2 = int(input("Enter the second number \n"))
        multiplication = num1 * num2
        print("The answer is:",multiplication)

    elif operation == "divide" or operation == "Divide" or operation == "division" or operation == "Division":
        num1 = int(input("Enter the first number \n"))
        num2 = int(input("Enter the second number \n"))
        division = num1 / num2
        print("The answer is:",division)

    elif operation == "square" or operation == "Square":
        num1 = int(input("Enter the number you would like to find the square of:\n"))
        square = num1 * num1
        print("The answer is:",square)

    elif operation == "divisibility" or operation == "Divisibility":
        num1 = int(input("Enter the number you would like to check is divisible by:\n"))
        num2 = int(input("Enter the number you would like :\n"))
        if num1%num2 == 0:
            print(f"{num1} is divisible by {num2}")
        elif num1%num2 != 0:
            print(f"{num1} is not divisible by {num2}")

    elif operation == "power" or operation == "Power":
        num1 = int(input("Enter the first number: \n"))
        num2 = int(input("Enter the second number: \n"))
        power = num1 ** num2
        print(f"{num1} to the power of {num2} is:\n",power)

def add(num1, num2):
    func_add = num1 + num2
    print("The answer is: \n", func_add)

def sub(num1, num2):
    func_sub = num1 - num2
    print("The answer is: \n", func_sub)

def mul(num1, num2):
    func_mul = num1 * num2
    print("The answer is: \n", func_mul)

def div(num1, num2):
    func_div = num1 / num2
    print("The answer is: \n", func_div)


def calculator():
    operation_selection = input("What operation would you like to perform? \n")

    if operation_selection in valid_operations:
        operation_validator = True

    else:
        operation_validator = False

    if operation_validator == True:
        run_calc(operation_selection)

    else:
        print("Please enter a valid operation and try again.")

