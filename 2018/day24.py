#
# Parse our format.
#
# 34846 too low

import sys
from pprint import pprint

class Unit(object):
    count = [0,0]
    def __init__(self,side,count,hp,immune,weak,damage,dtype,initiative):
        Unit.count[side] += 1
        self.side = side
        self.id = Unit.count[side]
        self.count = count
        self.hp = hp
        self.immune = immune
        self.weak = weak
        self.damage = damage
        self.dtype = dtype
        self.initiative = initiative
    def eff_power(self):
        return self.count * self.damage
    def damageto( self, defend ):
        if self.dtype in defend.immune:
            return 0
        damage = self.eff_power()
        if self.dtype in defend.weak:
            return damage+damage
        return damage
    def __repr__(self):
#        return '%d units each with %d hit points (immune to %s; weak to %s) with an attack that does %d %s at initiative %d' % (self.count, self.hp, ','.join(self.immune), ','.join(self.weak), self.damage, self.dtype, self.initiative)
#        return '%d x %d hp (immune:%s; weak:%s) %d %s initiative %d' % (self.count, self.hp, ','.join(self.immune), ','.join(self.weak), self.damage, self.dtype, self.initiative)
        return '%s %d: %d, %d hp %d %s init %d' % (("Immune","Infect")[self.side],self.id,self.count, self.hp, self.damage, self.dtype, self.initiative)

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

units = []
for ln in sys.stdin:
    if len(ln) < 2 or ln[0] == '#':
        continue
    if ln.startswith('Immune'):
        which = 0
    elif ln.startswith('Infect'):
        which = 1
    else:
        units.append( parse(ln, which) )

pprint(units)

def round( units ):
    print "\nAnother round\n"

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
        choices = list((dfd,att.damageto(dfd)) for dfd in units_left[att.side] )
        choices.sort( key=lambda c: (c[1],c[0].eff_power(),c[0].initiative) )
#        pprint(choices)
        if not choices: 
            continue
        dfd, damage = choices[-1]
        if damage:
            print att, "Chose", dfd, damage
            units_left[att.side].remove( dfd )
            attacks.append( (att, dfd, damage) )
        else:
            print att, "Chose no one"

    # The units attack in order by initiative.

    attacks.sort( key=lambda e: e[0].initiative, reverse=1 )
#    pprint(attacks)

    tot_damage = 0
    for attack in attacks:
        att, dfd, _ = attack
        if att not in units or dfd not in units:
            continue
        units_lost = att.damageto(dfd) // dfd.hp
        tot_damage += units_lost
        print att, "attacks"
        print "---", dfd, "lost", units_lost
        dfd.count -= units_lost
        if dfd.count <= 0:
            print "--- Eliminated"
            units.remove( dfd )
    return tot_damage

def count(units,side):
    return len(tuple(k for k in units if k.side==side))

def tryboost( units, boost ):
    for u in units:
        if u.side == 0:
            u.damage += boost
    while count(units,0) and count(units,1):
        if not round(units):
            break
    pprint(units)
    print "====", boost, sum( k.count for k in units)

import copy
for i in range(55,75):
    tryboost( copy.deepcopy(units), i )
