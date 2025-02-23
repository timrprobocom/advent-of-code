package main

import (
	"fmt"
	"math"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
029A
980A
179A
456A
379A`[1:]

var live string = `
973A
836A
780A
985A
413A`[1:]

//  //go:embed day20.txt
//  var live string

type Point = tools.Point

// This is faster than a map<char,point_t>.

/*
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
*/

func buttons(c byte) Point {
	switch c {
	case '7': return Point{0, 0}
	case '8': return Point{1, 0}
	case '9': return Point{2, 0}
	case '4': return Point{0, 1}
	case '5': return Point{1, 1}
	case '6': return Point{2, 1}
	case '1': return Point{0, 2}
	case '2': return Point{1, 2}
	case '3': return Point{2, 2}
	case 'X': return Point{0, 3}
	case '0': return Point{1, 3}
	case 'A': return Point{2, 3}
	}
	return Point{0, 0}
}

/*
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
*/

func dirpad(c byte) Point {
	switch c {
	case 'X': return Point{0, 0}
	case '^': return Point{1, 0}
	case 'A': return Point{2, 0}
	case '<': return Point{0, 1}
	case 'v': return Point{1, 1}
	case '>': return Point{2, 1}
	}
	return Point{0, 0}
}

type cache_t struct {
	pt0    Point
	pt1    Point
	robots int
}

/*
   bool operator<(const cache_t & other) const
   {
       return pt0 < other.pt0 || pt1 < other.pt1 || robots < other.robots;
   }
*/

var cache map[cache_t]int64

type Queue struct {
	pt Point
	s  string
}

// @cache
func cheapestAuxPad(pt0 Point, pt1 Point, robots int) int64 {
	nugget := cache_t{pt0, pt1, robots}
	if cache[nugget] > 0 {
		return cache[nugget]
	}

	var res int64 = math.MaxInt64
	var queue []Queue
	queue = append(queue, Queue{pt0, ""})

	for len(queue) > 0 {
		entry := queue[0]
		queue = queue[1:]
		if entry.pt == pt1 {
			res = min(res, cheapestRobot(entry.s+"A", robots-1))
			continue
		}
		if entry.pt == dirpad('X') {
			continue
		}
		if entry.pt.X < pt1.X {
			queue = append(queue, Queue{entry.pt.Add(Point{1, 0}), entry.s + ">"})
		}
		if entry.pt.X > pt1.X {
			queue = append(queue, Queue{entry.pt.Add(Point{-1, 0}), entry.s + "<"})
		}
		if entry.pt.Y < pt1.Y {
			queue = append(queue, Queue{entry.pt.Add(Point{0, 1}), entry.s + "v"})
		}
		if entry.pt.Y > pt1.Y {
			queue = append(queue, Queue{entry.pt.Add(Point{0, -1}), entry.s + "^"})
		}
	}
	cache[nugget] = res
	return res
}

func cheapestRobot(keys string, robots int) int64 {
	if robots == 0 {
		return int64(len(keys))
	}
	var sumx int64 = 0
	pt0 := dirpad('A')
	for _, c := range keys {
		pt1 := dirpad(byte(c))
		sumx += cheapestAuxPad(pt0, pt1, robots)
		pt0 = pt1
	}
	return sumx
}

func cheapest(pt0 Point, pt1 Point, botcount int) int64 {
	var res int64 = math.MaxInt64
	var queue []Queue
	queue = append(queue, Queue{pt0, ""})

	for len(queue) > 0 {
		entry := queue[0]
		queue = queue[1:]
		if entry.pt == pt1 {
			res = min(res, cheapestRobot(entry.s+"A", botcount))
			continue
		}
		if entry.pt == buttons('X') {
			continue
		}
		if entry.pt.X < pt1.X {
			queue = append(queue, Queue{entry.pt.Add(Point{1, 0}), entry.s + ">"})
		}
		if entry.pt.X > pt1.X {
			queue = append(queue, Queue{entry.pt.Add(Point{-1, 0}), entry.s + "<"})
		}
		if entry.pt.Y < pt1.Y {
			queue = append(queue, Queue{entry.pt.Add(Point{0, 1}), entry.s + "v"})
		}
		if entry.pt.Y > pt1.Y {
			queue = append(queue, Queue{entry.pt.Add(Point{0, -1}), entry.s + "^"})
		}
	}
	return res
}

func part1(data []string, bots int) int64 {
	var sumx int64 = 0
	for _, line := range data {
		var res int64 = 0
		pt0 := buttons('A')
		for _, c := range line {
			if DEBUG {
				fmt.Println("---", string(c), "---")
			}
			pt1 := buttons(byte(c))
			res += cheapest(pt0, pt1, bots)
			pt0 = pt1
		}
		if DEBUG {
			fmt.Println(res)
		}

		val := 0
		for _, c := range line {
			if tools.Isdigit(byte(c)) {
				val = val*10 + int(c) - '0'
			}
		}
		sumx += int64(val) * res
	}
	return sumx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	cache = make(map[cache_t]int64)

	fmt.Println("Part 1:", part1(data, 2))
	fmt.Println("Part 2:", part1(data, 25))
}
