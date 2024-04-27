from enum import Enum
import random

POSSIBLE_NUMBERS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"] # Only for refrence, DO NOT CHNAGE LATER

class Shape(Enum):
    HEART = 'H' # '♥'
    DIAMOND = 'D' # '♦'
    CLUB = 'C' # '♣'
    SPADE = 'S' #  '♠'

    def getShapeFromValue(value):
        for enum_member in Shape:
            if enum_member.value == value:
                return enum_member
        return None

class Card():
    
    def __init__(self, shape, number):
        self.shape = shape
        self.number = number

    def __str__(self):
        return f"{self.number}-{self.shape.value.encode('utf-8').decode('utf-8')}"
    

class Deck():
    
    def __init__(self):
        self.DECK = []

    def createDeck(self):
        self.DECK.clear()
        for s in Shape:
            for num in POSSIBLE_NUMBERS:
                self.DECK.append(Card(s, num))
        random.shuffle(self.DECK)

    def printDeck(self):
        print()
        items_per_line = 13
        for i in range(0, len(self.DECK), items_per_line):
            print(*self.DECK[i:i+items_per_line])
        print()


    def getTopCard(self):
        return self.DECK.pop(0)

    def pop(self, i):
        return self.DECK.pop(i)