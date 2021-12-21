import sys
import itertools
from collections import defaultdict, Counter

test = (4,8)
live = (9,10)

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = live

def part1(data):
    dice = itertools.cycle(range(1,101))
    score = [0,0]
    count = 0
    while True:
        p = count & 1
        turn = next(dice) + next(dice) + next(dice)
        count += 3
        data[p] = (data[p]+turn -1) % 10 + 1
        score[p] += data[p]
        if score[p] >= 1000:
            break
    if DEBUG:
        print(count, data, score)
    return(count * score[1-p])


def part2(data):
    # There are 7 possible outcomes of three dice, in a Gaussian curve.

    dice = list(Counter(
	i + j + k
	for i in (1,2,3)
	for j in (1,2,3)
	for k in (1,2,3)
    ).items())

    if DEBUG:
        print(dice)

    # Score, position, score, position, next player.
    universes = {(0, data[0], 0, data[1], 0): 1}
    wins = [0,0]

    # It takes 9 or 10 rolls to win.  The key trick is that, at each roll, there are 
    # only a few distinct states (at most about 11,000).  Many universes share the same 
    # state.  We need to track those counts.

    while universes:
        newu = defaultdict(int)
        # For each state (and many universes share the same state, that's the key):
        for state, cnt in universes.items():
            if DEBUG:
                print(state,cnt)
            #  Unpack the state.  The current player is always first.
            score, pos, others, otherp, turn = state

            for val, prob in dice:
                p = (pos + val - 1) % 10 + 1
                s = score + p
                if s >= 21:
                    wins[turn] += cnt * prob
                    continue

                # Swap positions for the next turn.
                newu[(others,otherp,s,p,1-turn)] += cnt * prob

        universes = newu
    return wins


print( "Part 1:", part1(list(data)) )
print( "Part 2:", max(part2(data)) )

