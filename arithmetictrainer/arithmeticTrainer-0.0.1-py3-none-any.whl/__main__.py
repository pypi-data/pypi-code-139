import functions as functions
def main():
    while True:
        question = functions.generate_question()
        functions.print_prompt(question[0], question[1], question[2])
        ans = int(input("Enter Your Answer: "))
        if (ans == question[3]):
            print("Correct")
        else:
            print("Incorrect")
        again = input("Another question? (Y/N): ")
        if(again != "Y"):
            break

if __name__ == "__main__":
    main()
