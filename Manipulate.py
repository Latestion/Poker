from Game import *
from Util import *
import itertools
import json

totalPlayers = int(input("Players: "))
game = PokerGame(totalPlayers)
game.getDeck().createDeck(False)

def inputCard():
    while True:
        x = input("Card (Ex - 10S [10 of Spade]): ").upper()
        if len(x) == 0 or x in ["NONE", "NULL"]:
            return None
        shape = Shape.getShapeFromValue(x[-1])
        if shape is None or x[:-1] not in POSSIBLE_NUMBERS:
            print("Invalid Card!")
            continue
        card = game.getDeck().getCard(shape, x[0:-1])
        if card is None:
            print("This card is already being used!")
            continue
        game.getDeck().DECK.remove(card)
        return card

def modifyHand(player):

    playerHand = game.getHands().get(player, [])
    game.getDeck().DECK.extend(playerHand)
    
    card1 = inputCard()
    card2 = inputCard()

    game.getHands()[player] = [card1, card2]

def modifyTable():

    pr, npr = "", ""
    for i in range(5):
        pr += ("None" if len(game.TABLE) <= i else str(game.TABLE[i])) + "\t"
        npr += str(i + 1) + "\t"
    print(f'{pr}\n{npr}')

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
    
    if len(game.TABLE) > card:
        game.getDeck().DECK.append(game.TABLE[card])

    modified = inputCard()

    if len(game.TABLE) > card:
        game.TABLE[card] = modified
    else:
        game.TABLE.append(modified)

while True:

    cls()
    print(f"Total Players: {totalPlayers}\n")
    option = int(input("Options:\n1. Player\n2. Table\n3. Calculate\n4. Exit\n5. Experimental\n"))

    if option == 5:

        TABLE_COMBINATIONS = itertools.combinations(game.deck.DECK, 5) 

        for comb in TABLE_COMBINATIONS:
            

            game.TABLE.extend(comb[0:-2])

            for card in game.TABLE:
                game.deck.DECK.remove(card)

            WINDICT = {
                3: {},
                4: {},
                5: {}
            } # TABLE_CARD: { [HAND]: (win, draw, loose) }

            for refer in range(3):
                
                PLAYER_COMBINATION = itertools.combinations(itertools.combinations(game.deck.DECK, 2), totalPlayers)
                key = refer + 3

                for pcomb in PLAYER_COMBINATION:

                    for player in range(totalPlayers):
                        game.HANDS[player] = list(pcomb[player])

                    game.winner()
                
                    for player in range(totalPlayers):
                    
                        hand = game.HANDS[player]
                        wins = WINDICT.get(key, {}).get(" ".join(map(str, hand)), {"wins": 0, "draws": 0, "loss": 0})
                
                        if player in game.WINNERS:
                            if len(game.WINNERS) > 1:
                                wins["draws"] += 1 # Draw
                            else: 
                                wins["wins"] += 1 # Win
                        else:
                            wins["loss"] += 1 # Loose

                        WINDICT[key][" ".join(map(str, hand))] = wins
                                
                if refer == 2: # No need to pop and add for 6th table card
                    break

                game.TABLE.append(comb[key])
                game.deck.DECK.remove(comb[key])
            
            with open("data/" + " ".join(map(str, comb[0:-2])), "w") as file:
                json.dump(dict, file)

            game.deck.createDeck(False)
            game.TABLE.clear()
        
    if option == 4:
        cls()
        print("Exited!")
        exit()

    elif option == 3:
        
        cls()
        print("Calculating all possible wins: ")
        print()

        COMBINATION = itertools.combinations(itertools.combinations(game.deck.DECK, 2), totalPlayers - 1)

        won = 0
        draw = 0
        totalGames = 0

        for comb in COMBINATION:

            # distribute the card
            for i in range(totalPlayers - 1):
                cards = list(comb[i])
                game.HANDS[i + 1] = cards

            game.winner()

            if 0 in game.WINNERS:
                if len(game.WINNERS) > 1:
                    draw += 1
                else:
                    won += 1 

            totalGames += 1

        print(f"Total Games: {totalGames}")
        print(f"Total Won: {won}")
        print(f"Total Draw: {draw}")
    
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
