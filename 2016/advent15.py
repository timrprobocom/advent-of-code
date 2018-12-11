#
# I believe there is a mathetmatical solution to this.  It's really 
# a Least Common Multiple problem.  But how do you integrate that
# with the current position?

import itertools

#cogs = ( (5, 4), (2, 1) )
cogs = ( (17, 1), (7, 0), (19, 2), (5, 0), (3, 0), (13, 5), (11, 0) )

for i in itertools.count():
    print i
    found = True
    for j,cog in enumerate(cogs):
        if (cog[1] + i + j + 1) % cog[0]:
            found = False
    if found:
        break

