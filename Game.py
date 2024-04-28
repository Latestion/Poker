import Deck
from Deck import *
from enum import Enum
from WinUtil import *

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

class PokerGame():

    def __init__(self, players):
        self.players = players
        self.HANDS = {}
        self.TABLE = []
        self.BURN_CARD = []
        self.WINNERS = []

        self.deck = Deck()
        self.deck.createDeck()

    def getDeck(self):
        return self.deck

    def getHands(self):
        return self.HANDS

    def distributeCards(self):
        for i in range(self.players):
            card = [self.deck.getTopCard(), self.deck.pop(self.players-1-i)] 
            self.HANDS.setdefault(i, card)

    def printHand(self, i):
        cards = self.HANDS.get(i)
        print(f'{str(i)}: {cards[0]}, {cards[1]}')

    def printAllHands(self):
        print("All player hands: ")
        for i in range(self.players):
            if i in self.HANDS:
                self.printHand(i)
            else:
                print(f"{i}: None, None")

    ############
    # Table Code
    ############

    def dealTableCards(self, totalCards):
        self.BURN_CARD.append(self.deck.getTopCard()) # BURN CARD

        for _ in range(totalCards):
            self.TABLE.append(self.deck.getTopCard())

    def printList(self, l):
        print(', '.join(map(str, l)))

    def comparePlayerCards(self, i):
        
        cards = self.HANDS.get(i)
        checkList = self.TABLE + cards
        
        highCard = getHighCard(checkList)
        num_pairs, pairs, num_triplets, triplets = get_pairs_and_triplets([card.number for card in checkList])
        quads = getRepeats(checkList, 4)
        straight = checkStraight(checkList)

        if len(triplets) > 1:
            indexList = [POSSIBLE_NUMBERS.index(num) for num in triplets]
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
                indexList = [POSSIBLE_NUMBERS.index(num) for num in pairs]
                pairs.pop(indexList.index(max(indexList)))
            return Win.FULL_HOUSE, (POSSIBLE_NUMBERS[min([POSSIBLE_NUMBERS.index(i) for i in triplets])], 
                                    POSSIBLE_NUMBERS[min([POSSIBLE_NUMBERS.index(i) for i in pairs])])
        if straight[1]:
            return Win.FLUSH, highCard
        
        if straight[0]:
            return Win.STRAIGHT, highCard
    
        if num_triplets >= 1: # if a player has 2 trios, it basically means they have a full house!
            tripletHighCard = [x for x in cards if x.number != triplets[0]]
            if len(tripletHighCard) == 0:
                tripletHighCard = [x for x in self.TABLE if x.number != triplets[0]]
            return Win.THREE_OF_A_KIND, (triplets[0], getHighCard(tripletHighCard))
        
        if num_pairs >= 2:

            X = [element for element in checkList if element.number not in pairs]
            
            if len(pairs) > 2:
                indexList = [POSSIBLE_NUMBERS.index(num) for num in pairs]
                pairs.pop(indexList.index(max(indexList)))

            return Win.TWO_PAIR, sorted(pairs, key=lambda x: POSSIBLE_NUMBERS.index(x)), getHighCard(X) # Returns the two highest pair!
        
        if num_pairs == 1:
            return Win.ONE_PAIR, pairs[0]
        
        return Win.HIGH_CARD, highCard

    def winner(self):
        save = []
        self.WINNERS = []
        print("Player Hand:")
        for i in range(self.players):
            data = self.comparePlayerCards(i)
            print(f'{str(i)}. {data[0].value[0]} -', data[1])
            save.append((i, data))
        
        print()

        save = sorted(save, key=lambda x : x[1][0].value[1])
        top = save[0][1][0]

        if top == Win.ROYAL or save[1][1][0] != top: # Checking for royal flush or top winner with unique shit
            print("Winner: ", end="")
            self.printWinner(save[0])
            self.WINNERS.append(save[0])
            return
        
        shared = [s for s in save if s[1][0] == top]
        
        if top in [Win.STRAIGHT_FLUSH, Win.FLUSH, Win.STRAIGHT, Win.HIGH_CARD, Win.ONE_PAIR, Win.FOUR_OF_A_KIND]:
            shared = sorted(shared, key=lambda x: POSSIBLE_NUMBERS.index(x[1][1]))
        elif top in [Win.FULL_HOUSE, Win.THREE_OF_A_KIND]:
            shared = sorted(shared, key=lambda x: (POSSIBLE_NUMBERS.index(x[1][1][0]), POSSIBLE_NUMBERS.index(x[1][1][1])))
        elif top == Win.TWO_PAIR:
            shared = sorted(shared, key=lambda x: (POSSIBLE_NUMBERS.index(x[1][1][0]), POSSIBLE_NUMBERS.index(x[1][1][1]), POSSIBLE_NUMBERS.index(x[1][2])))
        
        # Determine highest and high card for two pair hands
        highest = shared[0][1][1]
        highCard = shared[0][1][2] if top == Win.TWO_PAIR else None

        # Print winner(s)
        for s in shared:
            if s[1][1] == highest and (highCard is None or s[1][2] == highCard):
                print("Winner: ", end="")
                self.WINNERS.append(s)
                self.printWinner(s)

        print()
        print("Potential Competition: (HC = High Card)")
        for s in shared:
            self.printWinner(s)

    def printWinner(self, data):
        s = f'{data[0]} - {data[1][0].value[0]} - {data[1][1]}'
        if len(data[1]) == 3:
            s += " - HC: " + data[1][2]
        print(s)

    def saveWinner(self):
        with open("data\\" + ', '.join(map(str, self.TABLE)) + ".txt", "w") as f:

            w = ""
            for win in self.WINNERS:
                s = f'{win[0]} - {win[1][0].value[0]} - {win[1][1]}'
                if len(win[1]) == 3:
                    s += " - HC: " + win[1][2] + "\n"
                w += s

            f.write(
                f"All player hands: \n{[f'{str(i)}: {self.HANDS.get(i)[0]}, {self.HANDS.get(i)[1]}' for i in range(self.players)]}\nTable: \n{', '.join(map(str, self.TABLE))}\nWinners: \n{w}"
            )

if __name__ == "__main__":

    game = PokerGame(4)

    game.getDeck().createDeck()

    game.distributeCards()
    game.printAllHands()

    game.dealTableCards(3)
    game.dealTableCards(1)
    game.dealTableCards(1)

    print()
    print("Table:")
    game.printList(game.TABLE)
    print()

    game.winner()

