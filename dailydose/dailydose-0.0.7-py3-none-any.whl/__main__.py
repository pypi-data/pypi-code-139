from datetime import date
from dailydose import hang
from dailydose import fact
from dailydose import news
from dailydose import battleship


def main():
    run = True

    while run:
        today = date.today()
        print(f"{'*' * 20}")
        print(
            f"Today is {today.strftime('%Y-%m-%d')}. Feeling bored? How about...")

        print(f"\t 1. See a fun fact")
        print(f"\t 2. See a news")
        print(f"\t 3. Play hangman")
        print(f"\t 4. Play battleship")
        print(f"\t 5. <Quit>")

        user_selection = input("Choose a number 1-5...\n> ")
        while user_selection not in ["1", "2", "3", "4", "5"]:
            print("Wrong number...")
            user_selection = input("Choose a number 1-5...\n> ")

        if user_selection == "1":
            random_fact = fact.get()
            print(random_fact[0]['heading'])
            print("\n"+random_fact[0]['content'])

        elif user_selection == "2":

            choose = True
            while choose:
                print("Choose from the following subjects... ")
                print("1. Culture")
                print("2. Politics")
                print("3. Science")
                print("4. World")
                print("5. Technology")
                print("6. Environment")
                print("7. Business")
                print("8. <Return to main menu>")

                selection = input(
                    "Enter the number of the subject you want to explore: ")
                if selection not in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    print("Invalid selection. Please try again.")
                    continue
                else:
                    selection = int(selection)
                    choose = False

            if selection != 8:
                if selection == 1:
                    subject = "culture"
                    titular = "CULTURE"
                elif selection == 2:
                    subject = "policy-and-politics"
                    titular = "POLITICS AND POLICY"
                elif selection == 3:
                    subject = "science-and-health"
                    titular = "SCIENCE AND HEALTH"
                elif selection == 4:
                    subject = "world"
                    titular = "WORLD"
                elif selection == 5:
                    subject = "technology"
                    titular = "TECHNOLOGY"
                elif selection == 6:
                    subject = "energy-and-environment"
                    titular = "ENERGY AND ENVIRONMENT"
                elif selection == 7:
                    subject = "business-and-finance"
                    titular = "BUSINESS AND FINANCE"

                news.get_headlines(subject, titular)

            else:
                print("Returning to main menu...")

        elif user_selection == "3":
            number_of_letters = input("Choose the length of word 4-10:\n> ")
            hang.hangman(num_letter=number_of_letters)

        elif user_selection == "4":
            battleship.main()

        else:
            print("Bye!")
            run = False


if __name__ == '__main__':
    main()
