

class Point:
    """Simple 2-dimensional point."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<x={self.x},y={self.y}>"

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.length < other.length

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def dist(self,pt):
        return abs(self.x-pt.x) + abs(self.y-pt.y)

    def left(self):
        return Point(self.y,-self.x)

    def right(self):
        return Point(-self.y,self.x)
