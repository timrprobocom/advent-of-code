package main 
import ( 
	"os"
	"fmt" 
	"slices"
	"strings"

	"aoc/tools"
	pq "gopkg.in/dnaeon/go-priorityqueue.v1"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########`[1:]

var live string = `
#############
#...........#
###A#C#B#A###
  #D#D#B#C#
  #########`[1:]

type Point = tools.Point

// Either 7+2*4 (15) characters or 7+4*8 (23) characters.
type Node = string

// These are the assigned columns in the diagram.
var WAIT_COLS = []int{1, 2, 4, 6, 8, 10, 11}
var ROOM_COLS = []int{3, 5, 7, 9}

// These are the x,y coordinates of the waiting areas.
var WAITING_AREAS = []Point{ 
	Point{1,1}, Point{1,2}, Point{1,4}, Point{1,6}, Point{1,8}, Point{1,10}, Point{1,11} }

var PODS = "ABCD"
var COST = map[byte]int{ 'A': 1, 'B': 10, 'C': 100, 'D': 1000 }

var FINAL_NODE = Node("")

// A room sticks together.

func getRoomSize(node Node) int  {
	return (len(node) - 7) / 4
}

func setWaiting( node string, p int, c byte ) string {
	x := node[:p] + string(c) + node[p+1:]
	return x
}

func setRoomRow( node string, room int, row int, c byte ) string {
	per := getRoomSize(node)
	p := 7 + room * per + row
	return setWaiting( node, p, c )
}

func getRoomRow( node string, room int, row int ) byte {
	per := getRoomSize(node)
	p := 7 + room * per + row
	return node[p]
}

func getRoom( node string, room int ) string {
	per := (len(node)-7) / 4
	return node[7+room*per:7+(room+1)*per]
}

func testGetSet() {
	node := "A B C DABCDEFGH"
	fmt.Println( "row 1 in room 2 is F:", string(getRoomRow(node, 2, 1)) )
	fmt.Println( "row 0 in room 3 is G:", string(getRoomRow(node, 3, 0)) )
	node = setWaiting( node, 3, 'D')
	fmt.Println( "After set wait 3 to D:", node )
	node = setRoomRow( node, 1, 0, 'X' )
	fmt.Println( "After set room 1 row 0 to X:", node )
}

func wait_col_idx( col int ) int {
	switch col {
		case 1:
			return 0
		case 2, 4, 6, 8, 10:
			return col/2
		case 11:
		    return 6
	}
	return -1
}

// waiting contains 7 elements.
// rooms contains 2 or 4 rows of 4, depending on part 1 or 2.

func render(node Node) {
	if len(node) == 0 {
		return 
	}
	row := []byte("|...........|")
	for i := range 7 {
		c := node[i]
		row[WAIT_COLS[i]] = c
	}
	fmt.Println(string(row))

	row = []byte("++|.......|++")
    for i := range getRoomSize(node) {
		for j := range 4 {
			row[ROOM_COLS[j]] = getRoomRow(node,j,i) 
		}
		fmt.Println(string(row))
		row = []byte("  |.......|")
	}
}

// Parents is a map from Node to Node.
// ('', '', '', '', '', '', ''), (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))) 
// Which can easily be turned into a string.

func path_from_parents(parents map[Node]Node, end Node) []Node {
	out := []Node{end}
	for true {
		if DEBUG {
			fmt.Println(out[len(out)-1])
		}
		val, ok := parents[out[len(out)-1]]
		if !ok {
			break
		}
		out = append(out, val)
	}
	slices.Reverse(out)
    return out
}

type Cost struct {
	cost	int
	node	Node
}

func zero(s Node) int {
	return 0
}

// Adding a cost heuristic turns this from dijkstra to A*.
// from_node is a 7-element plus 4 2-element or 4-element.

func dijkstra( 
    from_node 	Node,
	expand 		func(Node)[]Cost,
	to_node 	Node,
	heuristic 	func(Node)int ) (map[Node]int, map[Node]Node) {

    /*
    expand should return an iterable of (cost, successor node) tuples.
    Returns (distances, parents).
    Use path_from_parents(parents, node) to get a path.
    */

	type Queue struct {
		delta 	int
		node 	Node
	}

    seen := make(map[Node]bool)
	g_values := make(map[Node]int)
    g_values[from_node] = 0

    parents := make(map[Node]string)

    // (f, g, n)
	todo := pq.New[Queue,int64](pq.MinHeap)
	todo.Put( Queue{0, from_node}, int64(heuristic(from_node)) )

    for !todo.IsEmpty() {
		nxt := todo.Get()
		//f := nxt.Priority
		g := nxt.Value.delta
		node := nxt.Value.node

        v, ok := g_values[node]
		if !ok {
			fmt.Println("Assert failed, node in g_values")
			os.Exit(-1)
		}
		if v > g {
			fmt.Println("Assert failed, g_values[node] <= g")
			os.Exit(-2)
		}

        if seen[node] {
            continue
		}

		if v != g {
			fmt.Println("Assert failed, g.values[node] == g")
			os.Exit(-3)
		}

		if node == to_node {
            break
		}

        seen[node] = true

        for _,cost := range expand(node) {
            new_g := g + cost.cost
			val,ok := g_values[cost.node]
            if !ok || new_g < val {
                parents[cost.node] = node
                g_values[cost.node] = new_g
				todo.Put( Queue{new_g, cost.node}, int64(new_g + heuristic(cost.node)) )
			}
		}
	}
    
    return g_values, parents
}

func get_path( 
	from_node Node,
	expand func(Node)[]Cost,
	to_node Node,
	heuristic func(Node) int) (int, []Node) {

    /*
    expand accepts a node and returns an iterable of (dist, successor node) 
    tuples.
    Returns (distance, path).
    */

    g_values, parents := dijkstra(from_node, expand, to_node, heuristic)
	_, ok := g_values[to_node]
    if ! ok {
        fmt.Println( "Assertion failed, couldn't reach to_node")
		os.Exit(-4)
	}
    return g_values[to_node], path_from_parents(parents, to_node)
}

// Is this path blocked?

func is_blocked( node Node, c1, c2 int ) bool {
    if c1 > c2 {
        c1, c2 = c2, c1
	}
	for col := c1+1; col < c2; col++ {
		idx := wait_col_idx(col)
		if idx >= 0 && node[idx] != ' ' {
            return true
		}
	}
    return false
}

// Given a node, this function returns the set of possible successor nodes
// and their incremental cost.

func expand( node Node ) []Cost {
    out := []Cost{}

    // Node should store waiting areas + rooms

    // If each room is filled with its pod, then we are done.
    // ('', '', '', '', '', '', ''), (('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'))) 
	// "       AABBCCDD"

	// This says:
	//  for each room in cur_rooms,
	//    if each row of the room is filled with corresponding PODS letter
	//      we win

	roomsize := getRoomSize(node)
	solved := true
    for i := range 4 {
		if getRoom(node,i) != strings.Repeat(string(PODS[i]),roomsize) {
			solved = false
			break
		}
	}
	if solved {
		return []Cost{Cost{0, FINAL_NODE}}
	}
    
    // First, see if we can move someone out of a room.

    empty := Point{}
	for i := range 4 {
		room := getRoom(node, i)
		// This is in screen coordinates, so first room is (2,2).
        to_move_coord := empty
		to_move := byte(' ')
		row := 0
		for row = range len(room) {
			to_move = room[row]
            if to_move != ' ' {
                to_move_coord = Point{2+row, ROOM_COLS[i]}
                break
			}
		}
        if to_move_coord == empty {
            continue
		}

        // Now find an empty spot.

        for j, waiting_area := range WAITING_AREAS {
            // Make sure spot is empty and path is not blocked.
			if node[j] == ' ' && !is_blocked(node, waiting_area.Y, to_move_coord.Y ) {

               // Have this person move over there.

				new_node := setWaiting( node, j, to_move )
				new_node = setRoomRow( new_node, i, row, ' ' )

				cost := tools.Mandist(to_move_coord, waiting_area) * COST[to_move]
				out = append( out, Cost{cost, new_node} )
			}
		}

		// Now see if we can move someone INTO a room.

		for j, waiting_area := range WAITING_AREAS {
			to_move := node[j]
			if to_move == ' ' {
				continue
			}

			target_room := int(to_move - 'A')
			target_room_contents := getRoom(node, target_room)

			// If the room is full, skip it.

			if target_room_contents[0] != ' ' {
				continue
			}

			// If their room has an empty row and is only filled by like things, use it.

			pick := true
			for _,c := range target_room_contents[1:] {
				pick = pick && (c == ' ' || byte(c) == to_move)
			}
			if !pick {
				continue
			}

			row := -1
			col := ROOM_COLS[target_room]
			if pick {
				// Find the empty row -- the lowest blank.
				// WHY is this "+2"?
				row = strings.LastIndex( target_room_contents, " " )
			}
			if row < 0 {
				fmt.Println( "Assertion failed, row >= 0" )
				os.Exit(-5)
			}

            if is_blocked(node, waiting_area.Y, col) {
                continue
			}
            
			new_node := setWaiting( node, j, ' ' )
			new_node = setRoomRow( new_node, target_room, row, to_move )

            cost := tools.Mandist(Point{row+2, col}, waiting_area) * COST[to_move]
			out = append( out, Cost{cost, new_node} )
		}
	}

    return out
}

func part1( part int, data []string ) int {
    extra := []string{"DD", "CB", "BA", "AC"}

	node := strings.Repeat(" ", len(WAITING_AREAS) )
    for i,room_col := range ROOM_COLS {
		node += string(data[2][room_col])
		if part == 2 {
			node += extra[i]
		}
        node += string(data[3][room_col])
	}

    if DEBUG {
        render(node)
	}

	empty := ""
    out, path := get_path(node, expand, FINAL_NODE, zero)
    if DEBUG {
		for _,p := range path {
			if p != empty {
				render(p)
			}
		}
	}

    return out
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println( "Part 1:", part1(1, data) )
  	fmt.Println( "Part 2:", part1(2, data) )
}
