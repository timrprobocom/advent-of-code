package main

import (
	"fmt"
	"strings"
	"time"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false


var test =`
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               `[1:]

var test2 = `
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     `[1:]


//go:embed day20.txt
var live string

type Point = tools.Point

var movements = []Point{ Point{0,-1},Point{0,1},Point{-1,0},Point{1,0} }


// Find the key points.


type Maze struct {
	maze	[]string
	w		int
	h		int
	paths	map[Point]Point
	gatesByPoint	map[Point]string
	gatesByCode	map[string]Point
	start	Point
	goal	Point
	outer	map[Point]bool
	inner	map[Point]bool
}

func MakeMaze( source []string ) *Maze {
	maze := Maze{}
	maze.maze = source
	w := len(maze.maze[4])
	h := len(maze.maze)
	maze.w = w
	maze.h = h

	gatesByPoint := make(map[Point]string)
	gatesByCode := make(map[string]Point)
	paths := make(map[Point]Point)

	for y := 2; y < h-2; y++ {
		for x := 2; x < w-2; x++ {
			if maze.maze[y][x] == '.' {
				for _,check := range []string {
					maze.maze[y][x-2:x],
					maze.maze[y][x+1:x+3],
					string(maze.maze[y-2][x])+string(maze.maze[y-1][x]),
					string(maze.maze[y+1][x])+string(maze.maze[y+2][x]),
				} {
					if 'A' <= check[0] && check[0] <= 'Z' && 'A' <= check[1] && check[1] <= 'Z' {
						pt := Point{x,y}
						if gate,ok := gatesByCode[check]; ok {
							paths[pt] = gate
							gatesByPoint[pt] = check
							paths[gate] = pt
						} else {
							gatesByCode[check] = pt
							gatesByPoint[pt] = check
						}
					}
				}
			}
		}
	}

	maze.gatesByCode = gatesByCode
	maze.gatesByPoint = gatesByPoint
	maze.paths = paths
	maze.start = maze.gatesByCode["AA"]
	maze.goal = maze.gatesByCode["ZZ"]

    maze.outer = make(map[Point]bool)
    maze.inner = make(map[Point]bool)
	for _,pt := range paths {
		if pt.X == 2 || pt.X == w-3 || pt.Y == 2 || pt.Y == h-3 {
			maze.outer[pt] = true
		} else {
			maze.inner[pt] = true
		}
	}

	return &maze
}

func (self *Maze) getpt( pt Point ) byte {
	// Allow indexing by a Point. 
	return self.maze[pt.Y][pt.X]
}


type SeenItem struct {
	pt Point
	level int
}

type QueueItem struct {
	pt Point
	dist int
	level int
}

func (self Maze) bfs( part int, start Point) int {
	seen := make(map[SeenItem]bool)
	unchecked := tools.Stack[QueueItem]{}
	unchecked.Push( QueueItem{start,0,0} )
	sec := time.Now()
	for !unchecked.IsEmpty() {
		q,_ := unchecked.PopFront()
		if DEBUG && time.Since(sec) > time.Second {
			sec = time.Now()
			fmt.Println( "Examine", q, unchecked.Size() )
		}
		if seen[SeenItem{q.pt,q.level}] {
			continue
		}
		if q.pt == self.goal && q.level == 0 {
			return q.dist
		}
		seen[SeenItem{q.pt,q.level}] = true
		newpt, ok := self.paths[q.pt]
		if ok {
			newlvl := q.level
			if part == 2 {
				if self.inner[q.pt] {
					newlvl ++
				} else {
					newlvl --
				}
			}
			if ! seen[SeenItem{newpt,newlvl}] {
				unchecked.Push( QueueItem{newpt,q.dist+1,newlvl} )
				continue
			}
		}
		for _,move := range movements {
			newpt := q.pt.Add(move)
			if !tools.Between( 0, newpt.X, self.w) || !tools.Between( 0, newpt.Y, self.h ) {
				continue
			}
			if self.outer[newpt] && q.level == 0 {
				continue
			}
			if seen[SeenItem{newpt,q.level}] {
				continue
			}
			if q.level > 0 && (newpt == self.start || newpt == self.goal) {
				continue
			}
			if self.getpt(newpt) == '.' {
				unchecked.Push( QueueItem{newpt,q.dist+1,q.level} )
			}
		}
	}
	return -1
}



func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	// Part 1.

	if input[len(input)-1] == '\n' {
		input = input[:len(input)-1]
	}
	maze := MakeMaze(strings.Split(input,"\n"))

	fmt.Println( "Part 1:", maze.bfs(1, maze.start) )

	// Part 2.

	if TEST {
		maze = MakeMaze(strings.Split(test2,"\n"))
	}

	fmt.Println( "Part 2:", maze.bfs(2, maze.start) )
}
