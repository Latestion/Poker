import Deck as deck # Importing this automatically runs the methods which are called in its code, soo dont call it again here!

players = int(input("Total Players: "))

# Player Hands

HANDS = {
    
}

def distributeCards():
    for i in range(players):
        card = [deck.getTopCard(), deck.DECK.pop(players-1-i)] # gets the top card and the next CARD THEY ARE SUPPOSED TO GET
        HANDS.setdefault(i, card)

def printHand(i):
    cards = HANDS.get(i)
    print(f'{str(i)}: {cards[0]}, {cards[1]}')

def printAllHands():
    for i in range(players):
        printHand(i)

distributeCards()
printAllHands()

############
# Table Code
############

TABLE = []
BURN_CARD = []

def dealFlop():
    BURN_CARD.append(deck.getTopCard()) # BURN CARD

    for _ in range(3):
        TABLE.append(deck.getTopCard())
    
def dealRiver():
    BURN_CARD.append(deck.getTopCard()) # BURN CARD
    TABLE.append(deck.getTopCard())

def printList(l):
    print(', '.join(map(str, l)))

def comparePlayerCards(i):
    
    cards = HANDS.get(i)
    

deck.printDeck()
dealFlop()
printList(TABLE)
printList(BURN_CARD)
