import sys
import heapq
from pprint import pprint

test = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

live = """\
#############
#...........#
###A#C#B#A###
  #D#D#B#C#
  #########"""

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = live.splitlines()

if DEBUG:
    sprint = print
else:
    def sprint(*a,**k):
        pass

# These are the assigned columns in the diagram.
WAIT_COLS = [1, 2, 4, 6, 8, 10, 11]
ROOM_COLS = [3, 5, 7, 9]

# These are the x,y coordinates of the waiting areas.
WAITING_AREAS = [ (1, x) for x in WAIT_COLS ]

PODS = 'ABCD'
COST = { "A": 1, "B": 10, "C": 100, "D": 1000 }

FINAL_NODE = tuple()

def render(waiting, rooms=None):
    def e(s):
        return s or '.'
    print( "(%s%s %s %s %s %s%s)" % tuple(map(e,waiting)) )
    for row in zip(*rooms):
        print( "   " + ' '.join(map(e,row)))

def path_from_parents(parents, end):
    out = [end]
    while out[-1] in parents:
        out.append(parents[out[-1]])
    out.reverse()
    return out

def psub(x, y):
    return [a-b for a, b in zip(x, y)]

def mandist1(x, y=None):
    if y: 
        x = psub(x, y)
    return sum(map(abs, x))

# Adding a cost heuristic turns this from dijkstra to A*.

def dijkstra( from_node, expand, to_node, heuristic=None ):
    """
    expand should return an iterable of (cost, successor node) tuples.
    Returns (distances, parents).
    Use path_from_parents(parents, node) to get a path.
    """
    if not heuristic:
        heuristic = lambda _: 0
    seen = set()
    g_values = {from_node: 0}
    parents = {}

    # (f, g, n)
    todo = [(0 + heuristic(from_node), 0, from_node)]

    while todo:
        f, g, node = heapq.heappop(todo)

        assert node in g_values
        assert g_values[node] <= g

        if node in seen:
            continue

        assert g_values[node] == g
        if to_node is not None and node == to_node:
            break
        seen.add(node)

        for cost, new_node in expand(node):
            new_g = g + cost
            if new_node not in g_values or new_g < g_values[new_node]:
                parents[new_node] = node
                g_values[new_node] = new_g
                heapq.heappush(todo, (new_g + heuristic(new_node), new_g, new_node))
    
    return (g_values, parents)

def get_path( from_node, expand, to_node, heuristic=None ):
    """
    expand accepts a node and returns an iterable of (dist, successor node) 
    tuples.
    Returns (distance, path).
    """
    g_values, parents = dijkstra(from_node, expand, to_node, heuristic)
    if to_node not in g_values:
        raise Exception("couldn't reach to_node")
    return (g_values[to_node], path_from_parents(parents, to_node))

# Is this path blocks?

def is_blocked( waits, c1, c2 ):
    if c1 > c2:
        c1, c2 = c2, c1
    for col in range(c1+1, c2):
        if col in WAIT_COLS and waits[WAIT_COLS.index(col)]:
            return True
    return False

# Given a node, this function returns the set of possible successor nodes
# and their incremental cost.

def expand(node):
    # (cost, node)
    out = []

    # Node should store waiting areas + rooms
    # waitings is a list of None or string
    cur_waitings, cur_rooms = node

    # If each room is filled with its pod, then we are done.

    if all(all(pod == x for x in room) for pod, room in zip(PODS,cur_rooms)):
        return [(0, FINAL_NODE)]
    
    # First, see if we can move someone out of a room.

    for i, room in enumerate(cur_rooms):
        to_move_coord = None
        for room_idx, to_move in enumerate(room):
            if to_move:
                to_move_coord = (2+room_idx, ROOM_COLS[i])
                break
        if not to_move_coord:
            continue

        # Now find an empty spot.

        for j, waiting_area in enumerate(WAITING_AREAS):
            # Make sure spot is empty and path is not blocked.
            if cur_waitings[j] or is_blocked(cur_waitings, waiting_area[1], to_move_coord[1]):
                continue

            # Have this person move over there.

            # list/map/list makes it writable.  tuple/map/tuple makes it hashable.
            new_waitings = list(cur_waitings)
            new_rooms = list(map(list, cur_rooms))

            new_waitings[j] = to_move
            new_rooms[i][room_idx] = ""

            cost = mandist1(to_move_coord, waiting_area) * COST[to_move]
            out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))


    # Now see if we can move someone INTO a room.

    for j, waiting_area in enumerate(WAITING_AREAS):
        to_move = cur_waitings[j]
        if not to_move:
            continue

        target_room = ord(to_move) - ord('A')
        target_room_contents = cur_rooms[target_room]

        # If their room has an empty row and is only filled by like things, use it.

        if target_room_contents[0] == "" and all(x == "" or x == to_move for x in target_room_contents[1:]):
            # Which column is this?
            col = ROOM_COLS[target_room]

            # Find the empty row.
            row = None
            for room_idx in range(len(target_room_contents))[::-1]:
                if target_room_contents[room_idx] == "":
                    row = room_idx + 2
                    break
            assert row

            if is_blocked(cur_waitings, waiting_area[1], col):
                continue
            
            new_waitings = list(cur_waitings)
            new_rooms = list(map(list, cur_rooms))

            new_waitings[j] = ""
            new_rooms[target_room][room_idx] = to_move

            cost = mandist1((row, col), waiting_area) * COST[to_move]
            out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))

    return out

def process(part,data):
    extra = ['']*4 if part == 1 else ["DD", "CB", "BA", "AC"]

    rooms = []
    for i,room_col in enumerate(ROOM_COLS):
        a, b = [data[row][room_col] for row in [2, 3]]
        rooms.append(tuple(a+extra[i]+b))

    rooms = tuple(rooms)
    waitings = ("",)*len(WAITING_AREAS)
    render(waitings, rooms)

    out, path = get_path((waitings, rooms), expand, FINAL_NODE)
    if DEBUG:
        [render(*p) for p in path if p]

    return out

print( "Part 1:", process(1,data) )
print( "Part 2:", process(2,data) )
