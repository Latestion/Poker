from enum import Enum
import random

class Shape(Enum):
    HEART = 'H' # '♥'
    DIAMOND = 'D' # '♦'
    CLUB = 'C' # '♣'
    SPADE = 'S' #  '♠'

class Card():
    
    def __init__(self, shape, number):
        self.shape = shape
        self.number = number

    def __str__(self):
        return f"{self.number}-{self.shape.value.encode('utf-8').decode('utf-8')}"
    
POSSIBLE_NUMBERS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"] # Only for refrence, DO NOT CHNAGE LATER

DECK = []

def createDeck():
    for s in Shape:
        for num in POSSIBLE_NUMBERS:
            DECK.append(Card(s, num))

def printDeck():
    print()
    items_per_line = 13
    for i in range(0, len(DECK), items_per_line):
        print(*DECK[i:i+items_per_line])
    print()


def shuffle():
    random.shuffle(DECK)

def getTopCard():
    return DECK.pop(0)
    
createDeck()
shuffle()