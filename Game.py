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

    consecutive = straight[0]
    same_shape = straight[1]
    royal = straight[2]

    if len(triplets) > 1:
        indexList = [deck.POSSIBLE_NUMBERS.index(num) for num in triplets]
        triplets.pop(indexList.index(max(indexList))) 
    
    if len(pairs) > 2:
        indexList = [deck.POSSIBLE_NUMBERS.index(num) for num in pairs]
        pairs.pop(indexList.index(max(indexList)))

    if consecutive:

        if royal and same_shape:
            return Win.ROYAL, highCard
        
        if same_shape:
            return Win.STRAIGHT_FLUSH, highCard

    if quads[0] == 1:
        return Win.FOUR_OF_A_KIND, quads[1][0]

    if num_pairs >= 1 and num_triplets >= 1:
        return Win.FULL_HOUSE, [triplets[0], deck.POSSIBLE_NUMBERS[min([deck.POSSIBLE_NUMBERS.index(i) for i in pairs])]] 
    
    if same_shape:
        return Win.FLUSH, highCard
    
    if consecutive:
        return Win.STRAIGHT, highCard
 
    if num_triplets >= 1: # if a player has 2 trios, it basically means they have a full house!
        return Win.THREE_OF_A_KIND, triplets[0]
    
    if num_pairs >= 2:
        return Win.TWO_PAIR, pairs # Returns the two highest pair!
    
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
printList(TABLE)
print()

def winner():
    save = []
    for i in range(players):
        data = comparePlayerCards(i)
        print(f'{str(i)}. {data[0].value[0]} -', data[1])
        save.append((i, data))

    save = sorted(save, key=lambda x : x[1][0].value[1])
    
    top = save[0][1][0]
    
    print(top)

    if top == Win.ROYAL or save[1][1][0] != top: # Checking for royal flush or top winner with unique shit
        print(f'Winner: {save[0]}')
        return
    
    if top == Win.FOUR_OF_A_KIND:
        if save[1][1][0] == top:
            print(f'Winner: {save[0]}')
            print(f'Winner: {save[1]}')
            return
        print(f'Winner: {save[0]}')
        return
    
    shared = []
    for s in save: 
        if s[1][0] == top:
            shared.append(s)
    
    if len(shared) > 1:
        if top == Win.STRAIGHT_FLUSH or top == Win.FLUSH or top == Win.STRAIGHT or top == Win.ONE_PAIR or top == Win.HIGH_CARD:
            shared = sorted(shared, key=lambda x: deck.POSSIBLE_NUMBERS.index(x[1][1]))
            print(f'Winner: {shared[0]}')
        

    print(shared)

winner()