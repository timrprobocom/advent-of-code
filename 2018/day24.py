#
# Parse our format.
#
# 34846 too low

import sys
from pprint import pprint
VERBOSE = "-v" in sys.argv

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
    #989,1274,fire,bludgeoning:slashing,25,slashing,3
    parts = ln.strip().split(',')
    return Unit(
        which,
        int(parts[0]),
        int(parts[1]),
        parts[2].split(':'),
        parts[3].split(':'),
        int(parts[4]),
        parts[5],
        int(parts[6])
    )


# Create the lists.

master = []
for ln in sys.stdin:
    if len(ln) < 2 or ln[0] == '#':
        continue
    if ln.startswith('Immune'):
        which = 0
    elif ln.startswith('Infect'):
        which = 1
    else:
        master.append( parse(ln, which) )

pprint(master)

def round( units ):
    if VERBOSE:
        print "\nAnother round\n"

    # Units choose who to attack in order of effective power and then by initiative.

    units.sort( key=lambda x: (x.eff_power(),x.initiative), reverse=1 )
    if VERBOSE:
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
        if VERBOSE:
            pprint(choices)
        if not choices: 
            continue
        dfd, damage = choices[-1]
        if damage:
            if VERBOSE:
                print att, "Chose", dfd, damage
            units_left[att.side].remove( dfd )
            attacks.append( (att, dfd, damage) )
        else:
            if VERBOSE:
                print att, "Chose no one"

    # The units attack in order by initiative.

    attacks.sort( key=lambda e: e[0].initiative, reverse=1 )
    if VERBOSE:
        pprint(attacks)

    tot_damage = 0
    for attack in attacks:
        att, dfd, _ = attack
        if att not in units or dfd not in units:
            continue
        units_lost = att.damageto(dfd) // dfd.hp
        tot_damage += units_lost
        if VERBOSE:
            print att, "attacks"
            print "---", dfd, "lost", units_lost
        dfd.count -= units_lost
        if dfd.count <= 0:
            if VERBOSE:
                print "--- Eliminated"
            units.remove( dfd )
    return tot_damage

def count(units,side):
    return any(k for k in units if k.side==side)

def tryboost( baseline, boosts ):
    units = [u.reset(boosts[u.side]) for u in baseline]
    while count(units,0) and count(units,1):
        if not round(units):
            break
    if VERBOSE:
        pprint(units)
    return sum( k.count for k in units)

# Part 1.

print "===== Part 1:", tryboost( master, (0,0) )

# Part 2.

# First, find the inflection point.

low, last = 0, 999999
for i in range(0,100,10):
    result = tryboost( master, (i,0) )
    if VERBOSE:
        print i, result
    if result > last:
        low = i-10
        break
    last = result

# Next, narrow it down.

if VERBOSE:
    print "Refining"
last = 999999
for i in range(low-10,low+10):
    result = tryboost( master, (i,0) )
    if VERBOSE:
        print i, result
    if result > last:
        low = i - 1
        break
    last = result

print "===== Part 2: (%d) %d" % (low, last)
