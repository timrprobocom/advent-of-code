package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test0 string = `
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############`[1:]

var test string = `
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################`[1:]


//go:embed day16.txt
var live string

type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

func (pt Point) left() Point {
	return Point{pt.y,-pt.x}
}

func (pt Point) right() Point {
	return Point{-pt.y,pt.x}
}


type PointSet = map[Point]bool

var start Point
var finish Point

type Queue struct {
	score int
	point Point
	dir Point
}

func part1( data []string, walls PointSet ) map[Point]int {
    // Do a simple BFS forward.

	queue := []Queue{ {0, start, Point{1,0}} }

    visited := make(map[Point]int)
	visited[start] = 0

	for len(queue) > 0 {
		e := queue[0]
		queue = queue[1:]
        if DEBUG {
            fmt.Print(e.score)
		}

		for _, d2 := range []Point{e.dir, e.dir.right(), e.dir.left()} {
			pain := 1001
			if d2 == e.dir {
				pain = 1
			}
			p2 := e.point.add( d2 )
			if !walls[p2] && (visited[p2] == 0 || visited[p2] > e.score+pain) {
				visited[p2] = e.score+pain
				queue = append( queue, Queue{e.score+pain, p2, d2} )
			}
		}
	}
    return visited
}

func part2( walls PointSet, visited map[Point]int ) int {
    // Do a backwards BFS.

    queue := []Queue{
		{visited[finish], finish, Point{-1,0}},
		{visited[finish], finish, Point{0,1}},
	}

    goods := make(PointSet)
    goods[finish] = true

	for len(queue) > 0 {
        e := queue[0]
		queue = queue[1:]
		for _, d2 := range []Point{e.dir, e.dir.right(), e.dir.left()} {
			pain := 1001
			if d2 == e.dir {
				pain = 1
			}
			p2 := e.point.add( d2 )
			if !walls[p2] && visited[p2] <= e.score-pain && !goods[p2] {
                queue= append( queue, Queue{e.score-pain, p2, d2} )
                goods[p2] = true
			}
		}
	}
    return len(goods)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")
	walls := make(PointSet)
	for y,row := range strings.Split(input,"\n") {
		for x,c := range row {
			if c == '#' {
				walls[Point{x,y}] = true
			} else if c == 'S' {
				start = Point{x,y}
			} else if c == 'E' {
				finish = Point{x,y}
			}
		}
	}

	visited := part1(data, walls)
	fmt.Println("Part 1:", visited[finish])
	fmt.Println("Part 2:", part2(walls, visited))
}

