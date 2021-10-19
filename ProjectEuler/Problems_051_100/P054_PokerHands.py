"""
In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.
The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example,
a pair of eights beats a pair of fives (see example 1 below).
But if two ranks tie, for example, both players have a pair of queens,
then highest cards in each hand are compared (see example 4 below); if the highest cards tie
then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand         Player 1         Player 2         Winner
1         5H 5C 6S 7S KD
Pair of Fives
     2C 3S 8S 8D TD
Pair of Eights
     Player 2
2         5D 8C 9S JS AC
Highest card Ace
     2C 5C 7D 8S QH
Highest card Queen
     Player 1
3         2D 9C AS AH AC
Three Aces
     3D 6D 7D TD QD
Flush with Diamonds
     Player 2
4         4D 6S 9H QH QC
Pair of Queens
Highest card Nine
     3D 6D 7H QD QS
Pair of Queens
Highest card Seven
     Player 1
5         2H 2D 4C 4D 4S
Full House
With Three Fours
     3C 3D 3S 9S 9D
Full House
with Three Threes
     Player 1

The file, poker.txt, contains one-thousand random hands dealt to two players.
Each line of the file contains ten cards (separated by a single space):
the first five are Player 1's cards and the last five are Player 2's cards.
You can assume that all hands are valid (no invalid characters or repeated cards),
each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
"""
import itertools

card_order = '123456789TJQKA'


def is_true_sequence(values):
    """Are card values in sequence?"""
    for i, j in zip(values, values[1:]):
        if i - 1 != j:
            return False
    return True


def is_flush_sequence(values):
    """Updated for A5342 as A2345 sequence."""
    if values == [card_value('AX'), card_value('5X'), card_value('4X'), card_value('3X'), card_value('2X')]:
        # Need card update on caller side - A card substituted by 1 card for proper comparison
        return True
    for i, j in zip(values, values[1:]):
        if i - 1 != j:
            return False
    return True


def sorter(cards):
    cards = sorted(cards, key=lambda c: card_order.index(c[0]), reverse=True)
    return cards


def cards_color(cards):
    return [c[1] for c in cards]


def cards_values(cards):
    return [card_order.index(c[0]) for c in cards]


def card_value(card):
    return card_order.index(card[0])


def remove_cards(cards, to_remove):
    result = []
    for card in cards:
        if not card in to_remove:
            result.append(card)
    return result


def royal_flush(cards):
    cards = sorter(cards)
    values = cards_values(cards)
    colors = cards_color(cards)
    if len(set(colors)) == 1 and values[-1] == card_value('TX') and values[0] == card_value("AX"):
        return True, cards, [], []
    return False, [], [], []


def straight_flush(cards):
    cards = sorter(cards)
    values = cards_values(cards)
    colors = cards_color(cards)
    if len(set(colors)) == 1 and is_flush_sequence(values):
        if card_value('2X') in values and card_value('AX') in values:
            cards[0] = '1X'
            cards = sorter(cards)
        return True, cards, [], []
    return False, [], [], []


def four_kind(cards):
    cards = sorter(cards)
    values = cards_values(cards)
    if values[0] == values[3]:
        return True, cards[:4], cards[4:], []
    if values[1] == values[4]:
        return True, cards[1:], cards[:1], []
    return False, [], [], []


def full_house(cards):
    cards = sorter(cards)
    values = cards_values(cards)
    if values[0] == values[2] and values[3] == values[4]:
        return True, cards[:3], cards[3:], []
    if values[0] == values[1] and values[2] == values[4]:
        return True, cards[2:], cards[:2], []
    return False, [], [], []


def flush(cards):
    cards = sorter(cards)
    colors = cards_color(cards)
    if len(set(colors)) == 1:
        return True, cards, [], []
    return False, [], [], []


def straight(cards):
    cards = sorter(cards)
    values = cards_values(cards)
    if is_flush_sequence(values):
        if card_value('2X') in values and card_value('AX') in values:
            cards[0] = '1X'
            cards = sorter(cards)
        return True, cards, [], []
    return False, [], [], []


def three_of_kind(cards):
    for c1, c2, c3 in itertools.combinations(cards, 3):
        if c1[0] == c2[0] == c3[0]:
            return True, [c1, c2, c3], sorter(remove_cards(cards, [c1, c2, c3])), []
    return False, [], [], []


def two_pairs(cards):
    pairs = []
    for c1, c2 in itertools.combinations(cards, 2):
        if c1[0] == c2[0]:
            pairs.append([c1, c2])
    if len(pairs) == 2:
        if card_value(pairs[0][0]) < card_value(pairs[1][0]):
            pairs = [pairs[1], pairs[0]]
        if pairs[0][0][0] == pairs[1][0][0]:
            raise ValueError
        return True, pairs[0], pairs[1], remove_cards(cards, [*pairs[0], *pairs[1]])
    return False, [], [], []


def one_pair(cards):
    for c1, c2 in itertools.combinations(cards, 2):
        if c1[0] == c2[0]:
            return True, [c1, c2], sorter(remove_cards(cards, [c1, c2])), []
    return False, [], [], []


def high_card(cards):
    return True, sorter(cards), [], []



rank_order = [
    royal_flush,
    straight_flush,
    four_kind,
    full_house,
    flush,
    straight,
    three_of_kind,
    two_pairs,
    one_pair,
    high_card,
]


def find_result(cards):
    for index, check in enumerate(rank_order):
        result, part1, part2, part3 = check(cards)
        if result:
            return -index, part1, part2, part3
    raise ValueError


def check_hands(hand1, hand2):
    # print('H1: ', hand1, 'H2: ', hand2)
    a0, a1, a2, a3 = find_result(hand1)
    b0, b1, b2, b3 = find_result(hand2)
    result1 = (a0, cards_values(a1), cards_values(a2), cards_values(a3))
    result2 = (b0, cards_values(b1), cards_values(b2), cards_values(b3))

    if result1 > result2:
        return 'Player 1'
    elif result1 < result2:
        return 'Player 2'
    else:
        raise ValueError


def hacker_main():
    t = int(input())
    for _ in range(t):
        cards = [s for s in input().split()]
        print(check_hands(cards[:5], cards[5:]))


def euler_main():
    counter = 0
    with open('P054_poker.txt', 'r') as file:
        for line in file.readlines():
            cards = [s for s in line.split()]
            result = check_hands(cards[:5], cards[5:])
            if result == 'Player 1':
                counter += 1
    print(counter)


# hacker_main()
euler_main()
