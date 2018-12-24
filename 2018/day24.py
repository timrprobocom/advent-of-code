#
# Parse our format.
#
# 34846 too low

from __future__ import print_function
import re
import sys

def empty( *args ):
    pass

if "-v" in sys.argv:
    dbgprint = print
    from pprint import pprint
else:
    dbgprint = empty
    pprint = empty

pat = r"(\d+) units each with (\d+) hit points (\([a-z;, ]+\) )?with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)$"

class Unit(object):
    count = [0,0]
    def __init__(self,side,count,hp,immune,weak,damage,dtype,initiative):
        Unit.count[side] += 1
        self.side = side
        self.id = Unit.count[side]
        self.count = count
        self.origCount = count
        self.hp = hp
        self.immune = immune
        self.weak = weak
        self.damage = damage
        self.origDamage = damage
        self.dtype = dtype
        self.initiative = initiative
    def eff_power(self):
        return self.count * self.damage
    def reset(self, boost=0):
        self.count = self.origCount
        self.damage = self.origDamage + boost
        return self
    def damageto( self, defend ):
        if self.dtype in defend.immune:
            return 0
        damage = self.eff_power()
        if self.dtype in defend.weak:
            return damage+damage
        return damage
    def __repr__(self):
#        return '%d units each with %d hit points (immune to %s; weak to %s) with an attack that does %d %s at initiative %d' % (self.count, self.hp, ','.join(self.immune), ','.join(self.weak), self.damage, self.dtype, self.initiative)
        return '%s %d: (n=%d hp=%d dam=%d init=%d)' % (("Immune","Infect")[self.side],self.id,self.count, self.hp, self.damage, self.initiative)


def parse(ln,which):
    gps = re.match(pat,ln)
    immune = []
    weak = []
    if gps.group(3):
        s = gps.group(3)[1:-2]
        for section in s.split(';'):
            parts = section.split()
            isimm = parts.pop(0) == 'immune'
            assert parts.pop(0)=='to'
            if isimm:
                immune = [k.strip(',') for k in parts]
            else:
                weak = [k.strip(',') for k in parts]

    return Unit(
        which,
        int(gps.group(1)),
        int(gps.group(2)),
        immune,
        weak,
        int(gps.group(4)),
        gps.group(5),
        int(gps.group(6))
    )

# Create the lists.

master = []
for ln in sys.stdin:
    ln = ln.strip()
    if len(ln) < 2 or ln[0] == '#':
        pass
    elif ln.startswith("Immune"):
        which = 0
    elif ln.startswith("Infect"):
        which = 1
    else:
        master.append( parse(ln,which) )

pprint(master)

def round( units ):
    dbgprint( "\nAnother round\n" )

    # Units choose who to attack in order of effective power and then by initiative.

    units.sort( key=lambda x: (x.eff_power(),x.initiative), reverse=1 )
    pprint(units)

    # Choose a defender.  For each unit, we choose the defender with the maximum damage
    # assessment, or if tied maximum effective power, or if tied maximum initiative.
    # A defender can only be attacked once.

    attacks = []
    units_left = (
        set(u for u in units if u.side==1),
        set(u for u in units if u.side==0)
    )
    for att in units:
        choices = [(dfd,att.damageto(dfd)) for dfd in units_left[att.side]]
        choices.sort( key=lambda c: (c[1],c[0].eff_power(),c[0].initiative) )
        pprint(choices)
        if not choices: 
            continue
        dfd, damage = choices[-1]
        if damage:
            dbgprint( att, "Chose", dfd, damage )
            units_left[att.side].remove( dfd )
            attacks.append( (att, dfd, damage) )
        else:
            dbgprint( att, "Chose no one" )

    # The units attack in order by initiative.

    attacks.sort( key=lambda e: e[0].initiative, reverse=1 )
    pprint(attacks)

    tot_damage = 0
    for attack in attacks:
        att, dfd, _ = attack
        if att not in units or dfd not in units:
            continue
        units_lost = att.damageto(dfd) // dfd.hp
        tot_damage += units_lost
        dbgprint( att, "attacks" )
        dbgprint( "---", dfd, "lost", units_lost )
        dfd.count -= units_lost
        if dfd.count <= 0:
            dbgprint( "--- Eliminated" )
            units.remove( dfd )
    return tot_damage

def count(units,side):
    return any(k for k in units if k.side==side)

def tryboost( baseline, boosts ):
    units = [u.reset(boosts[u.side]) for u in baseline]
    while count(units,0) and count(units,1):
        if not round(units):
            break
    pprint(units)
    return sum( k.count for k in units)

# Part 1.

print( "===== Part 1:", tryboost( master, (0,0) ) )

# Part 2.

# First, find the inflection point.

low, last = 0, 999999
for i in range(0,100,10):
    result = tryboost( master, (i,0) )
    dbgprint( i, result )
    if result > last:
        low = i-10
        break
    last = result

# Next, narrow it down.

dbgprint( "Refining" )
last = 999999
for i in range(low-10,low+10):
    result = tryboost( master, (i,0) )
    dbgprint( i, result )
    if result > last:
        low = i - 1
        break
    last = result

print( "===== Part 2: (%d) %d" % (low, last) )
