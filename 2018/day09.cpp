#include <list>

test = (
  (9, 25),
  (10, 1618),
  (13, 7999),
  (17, 1104),
  (21, 6111),
  (30, 5807)
)

test = (
  (10, 1618),
  (10, 16180)
)

live = ((448, 71628),)

data = test

void process( int npl, nmar )
{
    std::list<ring>
}

def process( npl, nmar ):
    ring = [0]
    keep = [0] * npl
    player = 0
    for m in range(1,nmar+1):
        if len(ring) == 1:
            ring = [m] + ring
        elif m % 23 == 0:
            print m, player, m, ring[-7]
            keep[player] += m + ring[-7]
            ring = ring[-6:] + ring[:-7]
        else:
            ring = [m] + ring[2:] + ring[:2]
#        print player+1, m, ring
        player = (player + 1) % npl
    print keep
    print max(keep)

process(*test[0])
process(*test[1])

#for run in live:
#    process(*run)
#    break


# So, you score once every 23.
# 23-1 % 9 = 5  gets 23 and  9
# 46-1 % 9 = 0  gets 46 and 17
# 69-1 % 9 = 6  gets 69 and 11
