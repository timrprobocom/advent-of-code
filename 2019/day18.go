package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

// Answer 8.
var test1 = []string{`
#########
#b.A.@.a#
#########`[1:],
// Answer 86.
`########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################`,
// Answer 136.
`#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################`,
// Answer 81.
`########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################`}

// Part 2, answer 72.
var test2 = []string{`
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############`[1:]}

//go:embed day18.txt
var live1 string

//go:embed day18b.txt
var live2 string

type Point = tools.Point

var movements = []Point{ Point{0,-1},Point{0,1},Point{-1,0},Point{1,0} }

var abs = tools.AbsInt[int]

func islower(c byte) bool {
	return 'a' <= c && c <= 'z' 
}

func isupper(c byte) bool {
	return 'A' <= c && c <= 'Z' 
}

func sub(s string, i int, c string) string {
    return s[0:i]+c+s[i+1:]
}

func ssort(s string) string {
	b := []byte(string)
	slices.Sort(b)
	return string(b)
}

type Maze struct {
	maze	[][]byte
	adit	[]Point
	size	int
}

func makeMaze(source []string) Maze {
	maze := Maze{}
	maze.maze = make([][]byte, len(source))
	maze.size = len(maze.maze)
	doors := make(map[byte]Point)
	keys := make(map[byte]bool)
	for y,ln := range source {
		maze.maze[y] = []byte(ln)
		for x := range len(ln) {
			ch := ln[x]
			if ch == '@' {
				maze.adit = append( maze.adit, Point{x,y} )
			} else if isupper(ch) {
				doors[ch] = Point{x,y}
			} else if islower(ch) {
				keys[ch] = true
			}
		}
	}
	
	// Eliminate any doors whose keys are not found in this maze.

	for k,v := range doors {
		if !keys[k+32] {
			maze.maze[v.Y][v.X] = '.'
		}
	}
	return maze
}

func (self Maze) print() {
	for _,row := range self.maze {
		fmt.Println(string(row))
	}
}

type Track struct {
	pt 		Point
	steps	int
	intheway []byte
}

func (self Maze) findall( start Point ) map[byte]Track {
	upcoming := make(map[Point][]byte)
	upcoming[start] = []byte{}
	visited := make(map[Point]bool)
	found := make(map[byte]Track)
	steps := 0

	for len(upcoming) > 0 {
		more := make(map[Point][]byte)
		for cur,intheway := range upcoming {
			ch := self.getpt(cur)
			if islower(ch) && steps > 0 {
				found[ch] = Track{cur, steps, intheway}
			}
			if isupper(ch) {
				intheway = append( intheway, ch )
			}
			visited[cur] = true
			for _,facing := range movements {
				next := cur.Add(facing)
				ch := self.getpt(next)
				if !visited[next] && ch != '#' {
					more[next] = intheway
				}
			}
		}
		upcoming = more
		steps ++
	}
	return found
}

func (maze Maze) getpt( pt Point ) byte {
	return maze.maze[pt.Y][pt.X]
}


// Stats key is char, value is (pt,steps,doors in the way)
//
// We need to do a depth-first search to weed out duplicates.

var seen map[string]int

func search( sitting string, found string ) int {
    if DEBUG {
        fmt.Println( "New search", sitting, found )
	}
    found = ssort(found)

    // If we've been in this situation before, we don't need to go again.
	if seen[sitting+found] > 0 {
        return seen[sitting+found]
	}

    paths = []

    // For each robot:
	for si := range len(sitting) {
		s := sitting[si]
        // For each key the robot can see:
        for k,v := range stats[s] {
            // If we've already picked it up, ignore.
            if found[k] {
                continue
			}
            _, dstep, doors = v
            // If there's a door in the way without a key, ignore.
// LEFT OFF
// need a found=galse for range doors if not lower in found
            if any( d.lower() not in found for d in doors ):
                continue
            // Go explore this path.
            paths.append( v.steps + search(sub(sitting,si,k), found+k) )
		}
	}
    ans = min(paths) if paths else 0
    if DEBUG {
        fmt.Println( sitting+found, ans )
	}
    seen[sitting+found] = ans
    return ans
}

// Divide the maze into four quadreants.

func split(grid []string) [][]string {
	grids := make([][]string,4)
    midh := len(grid)/2
    midw := len(grid[0])/2
    for _,row := range grid[:midh+1] {
        grids[0] = append(grids[0], row[:midw+1])
        grids[1] = append(grids[1], row[midw:])
	}
    for _,row := range grid[midh:] {
        grids[2] = append(grids[2], row[:midw+1])
        grids[3] = append(grids[3], row[midw:])
	}
    return grids
}


// Part 1

func part1(data string) int {
	return 0
}

// Part 2.

func part2(data string) int {
	return 0
}

// Splits a set of strings into a set of grids.

func subsplit( inx []string ) [][]string {
	out := make([][]string, len(inx))
	for i := range len(inx) {
		out[i] = strings.Split(inx[i],"\n")
	}
	return out
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup("", live1)

    data1 := [][]string{}
	data2 := [][]string{}
    if TEST {
		data1 = subsplit(test1)
		data2 = subsplit(test2)
	} else {
		data1 = [][]string{strings.Split(strings.TrimSpace(live1), "\n")}
		data2 = split(strings.Split(strings.TrimSpace(live2), "\n"))
	}

    sum := 0
	for _,grid := range data1 {
		maze := parse(grid)
		sumx += search(maze, '0','@')
	}

    sum := 0
	for _,grid = range data1 {
		maze := parse(grid)
		sumx += search(maze, '0','@')
	}
	fmt.Println("Part 2:", sum );
}

/*


def parse(s):
    global stats
    search.seen = {}
    maze = Maze(s)
    if DEBUG:
        maze.print()
        print( maze.adit )

# Find all of the targets.

    stats = {}
    for i,adit in enumerate(maze.adit):
        stats[str(i)] = maze.findall( adit )

    if DEBUG:
        print( sum(len(v) for v in stats.values() ))

# Find the distance betweeen targets.

    for v in list(stats.values()):
        for key,ptx in v.items():
            if key >= 'a':
                stats[key] = maze.findall(ptx[0])

    if DEBUG:
        pprint( stats )
*/
