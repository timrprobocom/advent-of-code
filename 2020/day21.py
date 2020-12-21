import os
import re
import sys
import functools
import itertools
import operator
from pprint import pprint

test = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".split('\n')

DEBUG = 'debug' in sys.argv
dprint = print if DEBUG else lambda *x: 0

if 'test' in sys.argv:
    data = test
else:
    data = open('day21.txt').read().split('\n')[:-1]

# Each ingredient contains 0 or 1 allergens.
# Each allergen is in exactly 1 ingredient.

def parse(data):
    for ln in data:
        a,_,b = ln.partition(' (contains ')
        yield a.split(), b[:-1].split(', ')

def process(data):

    # Ingredients contains each ingredient with a count of occurrences.

    ingredients = {}

    # Allergens contains each allergen with a set of the ingredients 
    # that might contain it.

    allergens = {}
    for left, right in parse(data):
        for i in left:
            if i not in ingredients:
                ingredients[i] = 0
            ingredients[i] += 1
        for i in right:
            if i not in allergens:
                allergens[i] = set(left)
            else:
                allergens[i] = allergens[i].intersection( set(left) )

    dprint( ingredients )
    dprint( allergens )

    # This is the list of all ingredients that might contain an allergen.

    for k,v in allergens.items():
        allergens[k] = list(v)

    known = set( k for v in allergens.values() for k in v )
    part1 = sum( v for k,v in ingredients.items() if k not in known )

    # Isolate the allergens which have only one possible ingredient.

    known = []
    while 1:

        # Find any entries that are down to one ingredient.

        singles = [ k for k,v in allergens.items() if len(v) == 1 ]
        if not singles:
            break

        known.extend( (k, allergens[k][0]) for k in singles )

        # Remove the singles from the remaining allergen list.

        for k,v in allergens.items():
            for _,k1 in known:
                if k1 in v:
                    allergens[k].remove(k1)

    # Combine the ingredients, sorted by their allergens.

    known.sort()
    dprint( known )
    mylist = ','.join( k[1] for k in known )
    
    return part1, mylist

p1, p2 = process(data)
print( "Part 1:", p1 )
print( "Part 2:", p2 )
