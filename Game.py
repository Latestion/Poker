import Deck as deck # Importing this automatically runs the methods which are called in its code, soo dont call it again here!
from enum import Enum
from Deck import *
from collections import Counter

class Win(Enum):
    ROYAL = "Royal Flush", 1
    STRAIGHT_FLUSH = "Straight Flush", 2
    FOUR_OF_A_KIND = "Four of a kind", 3
    FULL_HOUSE = "Full House", 4
    FLUSH = "Flush", 5
    STRAIGHT = "Straight", 6
    THREE_OF_A_KIND = "Three of a kind", 7 
    TWO_PAIR = "Two Pair", 8
    ONE_PAIR = "One Pair", 9
    HIGH_CARD = "High Card", 10

players = 6 # int(input("Total Players: "))

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
    print("All player hands:")
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
    
def dealTurnOrRiver():
    BURN_CARD.append(deck.getTopCard()) # BURN CARD
    TABLE.append(deck.getTopCard())

def printList(l):
    print(', '.join(map(str, l)))

def comparePlayerCards(i):
    
    cards = HANDS.get(i)
    checkList = TABLE + cards
    
    highCard = getHighCard(checkList)
    num_pairs, pairs, num_triplets, triplets = get_pairs_and_triplets([card.number for card in checkList])
    quads = getRepeats(checkList, 4)
    straight = checkStraight(checkList)

    if len(triplets) > 1:
        indexList = [deck.POSSIBLE_NUMBERS.index(num) for num in triplets]
        triplets.pop(indexList.index(max(indexList))) 

    if straight[0]:
        if straight[2] and straight[1]:
            return Win.ROYAL, highCard
        if straight[1]:
            return Win.STRAIGHT_FLUSH, highCard
        
    if quads[0] == 1:
        return Win.FOUR_OF_A_KIND, quads[1][0]

    if num_pairs >= 1 and num_triplets >= 1:
        if len(pairs) > 2:
            indexList = [deck.POSSIBLE_NUMBERS.index(num) for num in pairs]
            pairs.pop(indexList.index(max(indexList)))
        return Win.FULL_HOUSE, (deck.POSSIBLE_NUMBERS[min([deck.POSSIBLE_NUMBERS.index(i) for i in triplets])], 
                                deck.POSSIBLE_NUMBERS[min([deck.    POSSIBLE_NUMBERS.index(i) for i in pairs])])
    if straight[1]:
        return Win.FLUSH, highCard
    
    if straight[0]:
        return Win.STRAIGHT, highCard
 
    if num_triplets >= 1: # if a player has 2 trios, it basically means they have a full house!
        tripletHighCard = [x for x in cards if x.number != triplets[0]]
        if len(tripletHighCard) == 0:
            tripletHighCard = [x for x in TABLE if x.number != triplets[0]]
        return Win.THREE_OF_A_KIND, (triplets[0], getHighCard(tripletHighCard))
    
    if num_pairs >= 2:

        X = [element for element in checkList if element.number not in pairs]
         
        if len(pairs) > 2:
            indexList = [deck.POSSIBLE_NUMBERS.index(num) for num in pairs]
            pairs.pop(indexList.index(max(indexList)))

        return Win.TWO_PAIR, sorted(pairs, key=lambda x: deck.POSSIBLE_NUMBERS.index(x)), getHighCard(X) # Returns the two highest pair!
    
    if num_pairs == 1:
        return Win.ONE_PAIR, pairs[0]
    
    return Win.HIGH_CARD, highCard

def get_pairs_and_triplets(numbers):
    counts = Counter(numbers)
    pairs = []
    triplets = []
    used_numbers = set()  # To keep track of numbers already used in pairs or triplets
    
    # Find triplets
    for num, count in counts.items():
        if count >= 3:
            triplets.append(num)
            used_numbers.add(num)
    
    # Find pairs (excluding numbers used in triplets)
    for num, count in counts.items():
        if count >= 2 and num not in used_numbers:
            pairs.append(num)
    
    return len(pairs), pairs, len(triplets), triplets

def getRepeats(card_list, i):
    numbers = [card.number for card in card_list]
    counts = Counter(numbers)
    quads = [(num, count // i) for num, count in counts.items() if count >= i]
    num_quads = sum(count for num, count in quads)
    return num_quads, [num for num, count in quads]

def checkStraight(card_list):
    consecutive = False
    same_shape = False
    royal = False
    
    shapes = {card.shape for card in card_list}
    if len(shapes) == 1:
        same_shape = True

    numbers = [card.number for card in card_list]

    if "A" in numbers and "2" in numbers and "3" in numbers and "4" in numbers and "5" in numbers:
        consecutive = True
    elif "A" in numbers and "K" in numbers and "Q" in numbers and "J" in numbers and "10" in numbers:
        consecutive = True
        royal = True
    else:
        for i in range(len(card_list) - 4):
            if all(
                POSSIBLE_NUMBERS.index(card_list[i + j].number) ==
                    POSSIBLE_NUMBERS.index(card_list[i].number) + j
                for j in range(5)
            ):
                consecutive = True
                break

    return consecutive, same_shape, royal

def getHighCard(card_list):
    numbers = [deck.POSSIBLE_NUMBERS.index(card.number) for card in card_list]
    return deck.POSSIBLE_NUMBERS[min(numbers)]
    
dealFlop()
dealTurnOrRiver()
dealTurnOrRiver()

print()
print("Table:")
printList(TABLE)
print()

def winner():
    save = []
    print("Player Hand:")
    for i in range(players):
        data = comparePlayerCards(i)
        print(f'{str(i)}. {data[0].value[0]} -', data[1])
        save.append((i, data))
    
    print()

    save = sorted(save, key=lambda x : x[1][0].value[1])
    top = save[0][1][0]

    if top == Win.ROYAL or save[1][1][0] != top: # Checking for royal flush or top winner with unique shit
        print("Winner: ", end="")
        printWinner(save[0])
        return
    
    shared = [s for s in save if s[1][0] == top]
    
    if top in [Win.STRAIGHT_FLUSH, Win.FLUSH, Win.STRAIGHT, Win.HIGH_CARD, Win.ONE_PAIR, Win.FOUR_OF_A_KIND]:
        shared = sorted(shared, key=lambda x: deck.POSSIBLE_NUMBERS.index(x[1][1]))
    elif top in [Win.FULL_HOUSE, Win.THREE_OF_A_KIND]:
        shared = sorted(shared, key=lambda x: (deck.POSSIBLE_NUMBERS.index(x[1][1][0]), deck.POSSIBLE_NUMBERS.index(x[1][1][1])))
    elif top == Win.TWO_PAIR:
        shared = sorted(shared, key=lambda x: (deck.POSSIBLE_NUMBERS.index(x[1][1][0]), deck.POSSIBLE_NUMBERS.index(x[1][1][1]), deck.POSSIBLE_NUMBERS.index(x[1][2])))
    
    # Determine highest and high card for two pair hands
    highest = shared[0][1][1]
    highCard = shared[0][1][2] if top == Win.TWO_PAIR else None

    # Print winner(s)
    for s in shared:
        if s[1][1] == highest and (highCard is None or s[1][2] == highCard):
            print("Winner: ", end="")
            printWinner(s)

    print()
    print("Potential Competition: (HC = High Card)")
    for s in shared:
        printWinner(s)

def printWinner(data):
    s = f'{data[0]} - {data[1][0].value[0]} - {data[1][1]}'
    if len(data[1]) == 3:
        s += " - HC: " + data[1][2]
    print(s)

winner()