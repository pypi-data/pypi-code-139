import RockPaperScissorsFullGame.RPS as RPS
# import RPS


def main():
    #first ask user if they want to see ascii art
    asciiVisibility = RPS.setAsciiVisibility()
    
    # game
    play = True
    while (play):
        computerItem = RPS.getComputerItem()
        playerInput = input("Enter your item: (rock, paper, scissors)\n")
        if(playerInput.lower() == "quit"):
            print("Thank you for playing!\n")
            break
        else:
            playerItem = RPS.inputToItem(playerInput)
            if(playerItem == None):
                print("Invalid Input\n")
                continue
            else:
                playerMove = RPS.getPlayerAsciiArt(playerItem)
                computerMove = RPS.getComputerAsciiArt(computerItem)
                if(not asciiVisibility):
                    print("You choose " + playerItem.name + ". Computer chooses " + computerItem.name + ".")
                else:
                    print("Player Move: " + playerItem.name + playerMove)
                    print("Computer Move: " + computerItem.name + computerMove)
                result = RPS.getOutcome(playerItem,computerItem)
                print("You " + result.name + ".\n")



if __name__ == '__main__':
    main()