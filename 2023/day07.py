import os
import sys
from collections import Counter

test = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

order = '23456789TJQKA'

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open(day+'.txt').readlines()

DEBUG = 'debug' in sys.argv

#6 Five of a kind, where all five cards have the same label: AAAAA
#5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
#4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
#3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
#2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
#1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
#0 High card, where all cards' labels are distinct: 23456

def grade(hand):
    value = list(order.index(c) for c in hand)
    cts = Counter(hand)
    # For pass 2, replace the joker by the most common card.
    if order[0] == 'J' and 'J' in hand:
        pick = 'J'
        for c in  cts.most_common(2):
            if c[0] != 'J':
                pick = c[0]
                break
        hand = hand.replace('J',pick)
        cts = Counter(hand)
    vals = list(cts.values())
    vals.sort(reverse=True)

    if len(vals) == 1:
        return [6]+value
    if len(vals) == 2:
        if vals[0] == 4:
            return [5]+value
        return [4]+value
    if len(vals) == 3:
        if vals[0] == 3:
            return  [3]+value
        return [2]+value
    if len(vals) == 4:
        return [1]+value
    if len(vals) == 5:
        return [0]+value


def part1(data):
   hands = []
   for row in data:
       hand,bid = row.split()
       score = grade(hand)
       hands.append( (score,hand,int(bid)) )
   hands.sort()
   if DEBUG:
       for n,h in enumerate(hands):
           print(n+1, h, (n+1)*h[2])
   return sum((n+1)*h[2] for n,h in enumerate(hands))

print("Part 1:", part1(data))
order = 'J23456789TQKA'
print("Part 2:", part1(data))
