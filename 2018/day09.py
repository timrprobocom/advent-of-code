
test = (
  (9, 25),
  (10, 1618),
  (13, 7999),
  (17, 1104),
  (21, 6111),
  (30, 5807)
)

live = (
    (448, 71628),
    (448, 7162800)
)

class Marble(object):
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def add( self, new ):
        if new.value % 23 == 0:
            away = self
            for _ in range(7):
                away = away.prev
# Remove
            away.next.prev = away.prev
            away.prev.next = away.next
            return away.next, new.value + away.value
        else:
            next1 = self.next
            next2 = next1.next
            new.next = next2
            new.prev = next1
            next1.next = new
            next2.prev = new
            return new, 0

def process( npl, nmar ):
    nextval = 0
    latest = Marble(nextval)
    score = [0] * npl
    player = 0

    while latest.value < nmar:
        nextval += 1
        latest, points = latest.add( Marble(nextval) )
        score[player] += points
        player = (player + 1) % npl

    while latest.prev:
        n = latest.next
        latest.prev = None
        latest.next = None
        latest = n
    
    return max(score)

for t in test:
    print t, process(*t)
for t in live:
    print t, process(*t)
