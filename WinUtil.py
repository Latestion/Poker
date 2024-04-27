from collections import Counter
from Deck import *

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
    numbers = [POSSIBLE_NUMBERS.index(card.number) for card in card_list]
    return POSSIBLE_NUMBERS[min(numbers)]