from Game import *
from Util import *

totalPlayers = int(input("Players: "))
game = PokerGame(totalPlayers)

USED = []

def inputCard():
    x = input("Card (Ex - 10S [10 of Spade]): ").upper()
    x = None if len(x) == 0 or x in ["NONE", "NULL"] else (Shape.getShapeFromValue(x[-1]), x[0:-1])
    if x is not None and (x[0] == None or x[1] not in POSSIBLE_NUMBERS):
        print("Invalid Card!")
        return inputCard()
    elif x is not None:
        card = Card(x[0], x[1])
        if card in USED:
            print("This card is already being used!")
            return inputCard()
        return card
    return None 

def modifyHand(player):

    player_hand = game.getHands().get(player, [])
    
    global USED
    USED = list(set(USED) - set(player_hand))

    card1 = inputCard()
    card2 = inputCard()
    USED.append(card1)
    USED.append(card2)

    game.getHands()[player] = [card1, card2]

def modifyTable():

    pr = ""
    npr = ""
    for i in range(5):
        pr += ("None" if len(game.TABLE) <= i else str(game.TABLE[i])) + "\t"
        npr += str(i + 1) + "\t"
    print(pr)
    print(npr)

    card = int(input("Card: ")) - 1

    if card > len(game.TABLE):
        cls()
        print("You cannot edit this card!")
        modifyTable()
        return
    
    for i in range(card):
        if game.TABLE[i] == None:
            cls()
            print("You cannot edit this card!")
            modifyTable()
            return
    
    modified = inputCard()

    if len(game.TABLE) > card:
        game.TABLE[card] = modified
    else:
        game.TABLE.append(modified)

while True:

    cls()
    print(f"Total Players: {totalPlayers}\n")
    option = int(input("Options:\n1. Player\n2. Table\n3. Calculate\n4. Exit\n"))
    
    if option == 4:
        cls()
        print("Exited!")
        exit()

    elif option == 2:
        
        while True:

            cls()
            print("TABLE:", "None, None, None, None, None" if len(game.TABLE) == 0 else ', '.join(map(str, game.TABLE)), sep="\n")
            print()

            if input("Do you want to modify the table (Y/N)? ").upper() == "Y":
                cls()
                modifyTable()
            else:
                break

    elif option == 1:
        
        while True:

            cls()
            game.printAllHands()
            player = int(input("\nSelect Player (-1 to Exit): "))

            if player >= totalPlayers or player < 0:
                if player == -1:
                    break
                print("Invalid Player!")
                continue
            
            cls()
            
            HAND = game.getHands()

            if player in HAND:
                game.printHand(player)
                while True:
                    if input("Do you want to modify this hand (Y/N)? ").upper() == "Y":
                        modifyHand(player)
                    break
            else:
                modifyHand(player)
