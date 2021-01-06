import os
import sys
import itertools
import copy

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

spells = 'mdspr'

cost = { 'm': 53, 'd': 73, 's': 113, 'p': 173, 'r': 229 }

def around( part, boss, player, mana, remains, spell ):
    global minmana
    bhp,bdam = boss
    php,parm,pmana = player
    rp,rs,rr = remains

    # If we can't afford it, dead end.

    fee = cost[spell[-1]]
    if fee > pmana:
        return

    mana += fee
    pmana -= fee

    # If we've already spent too much, dead end.

    if mana >= minmana:
        return

    # Cast a spell.

    if spell[-1] == 'm':
        bhp -= 4
    elif spell[-1] == 'd':
        bhp -= 2
        php += 2
    elif spell[-1] == 's':
        rs = 6
    elif spell[-1] == 'p':
        rp = 6
    elif spell[-1] == 'r':
        rr = 5

    for turn in (0,1):

        # Spell effects for boss/player turn.

        if rp:
            bhp -= 3
            rp -= 1

        if rs:
            parm = 7
            rs -= 1
        else:
            parm = 0

        if rr:
            pmana += 101
            rr -= 1

        if bhp <= 0:
            dprint( spell, mana )
            minmana = mana
            return

        if turn:
            break

        # Boss attacks.

        php -= bdam - parm

        # Player's turn starts.

        if part == 2:
            php -= 1
        if php <= 0:
            return

    # Try each spell.

    for i in spells:
        around( part, (bhp,bdam), (php,parm,pmana), mana, (rp,rs,rr), spell+i )

minmana = 9999
for i in spells:
    around( 1, (55,8), (50,0,500), 0, (0,0,0), i )

print( "Part 1:", minmana )

minmana = 99999
for i in spells:
    around( 2, (55,8), (49,0,500), 0, (0,0,0), i )

print( "Part 2:", minmana )
