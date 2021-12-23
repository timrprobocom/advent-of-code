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

WAITING_AREAS = [
    (1, x)
    for x in [1, 2, 4, 6, 8, 10, 11]
]

WTF = [1, 2, 4, 6, 8, 10, 11]

ROOM_COLS = [3,5,7,9]

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

def expand(node):
    # (weight, node)
    out = []

    # node should store waiting areas + rooms
    cur_waitings, cur_rooms = node

    # waitings is a list of None or string
    if all(all(chr(ord('A')+i) == x for x in room) for i, room in enumerate(cur_rooms)):
        return [(0, FINAL_NODE)]
    
    for i, room in enumerate(cur_rooms):
        # find the thing to move
        # sprint(room)
        for room_idx, to_move in enumerate(room):
            if to_move == "":
                continue
            to_move_coord = (2+room_idx, ROOM_COLS[i])
            break
        else:
            continue

        for j, waiting_area in enumerate(WAITING_AREAS):
            if cur_waitings[j] == "":
                # CHECK IF BLOCKED OFF.
                c1, c2 = waiting_area[1], to_move_coord[1]
                if c1 > c2:
                    c1, c2 = c2, c1
                bad = False
                for col in range(c1+1, c2):
                    if col in WTF and cur_waitings[WTF.index(col)] != "":
                        bad = True
                        break
                if bad:
                    continue

                # have this person move over there
                new_waitings = list(cur_waitings)
                new_rooms = list(map(list, cur_rooms))

                cost = mandist1(to_move_coord, waiting_area) * COST[to_move]
                new_waitings[j] = to_move
                new_rooms[i][room_idx] = ""
                out.append((cost, (tuple(new_waitings), tuple(map(tuple, new_rooms)))))
    
    # Move from waiting to room
    for j, waiting_area in enumerate(WAITING_AREAS):
        to_move = cur_waitings[j]
        if to_move == "":
            continue
        target_room = ord(to_move) - ord('A')
        target_room_actual = cur_rooms[target_room]
        # first, then second
        if target_room_actual[0] == "" and all(x == "" or x == to_move for x in target_room_actual[1:]):
            # move in
            col = ROOM_COLS[target_room]
            # go back
            for room_idx in range(len(target_room_actual))[::-1]:
                if target_room_actual[room_idx] != "":
                    continue
                row = room_idx + 2
                break
            else:
                assert False

            # CHECK IF BLOCKED OFF.
            c1, c2 = waiting_area[1], col
            if c1 > c2:
                c1, c2 = c2, c1
            bad = False
            for col2 in range(c1+1, c2):
                if col2 in WTF and cur_waitings[WTF.index(col2)] != "":
                    bad = True
                    break
            if bad:
                continue
            
            cost = mandist1((row, col), waiting_area) * COST[to_move]

            new_waitings = list(cur_waitings)
            new_rooms = list(map(list, cur_rooms))

            new_waitings[j] = ""
            new_rooms[target_room][room_idx] = to_move
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
