
# Based on what we learned in 2019 day 22, this becomes trivial.

first = 20151125
mult = 252533
modulo = 33554393

row = 2981
col = 3075

# Row 1 col 3075 is sum(1..3075), (N)(N+1)/2.
# Row 2981 col 3075 would be in the diagonal ending at col 3074 + 2981 - 1
# and it's 2981 - 1 entries prior to that.

diagonal = col + row - 1
entry = (diagonal * (diagonal+1)) // 2 - row + 1

# Now, we need first x entry ^ mult.  We know how to do that.

print( "Part 1:", (first * pow( mult, entry-1, modulo )) % modulo )

