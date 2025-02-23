package main

import (
	"container/heap"
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533`[1:]

//go:embed day17.txt
var live string

var WIDTH = -1
var HEIGHT = -1

type Point = tools.Point

var N Point = Point{0, -1}
var E Point = Point{1, 0}
var S Point = Point{0, 1}
var W Point = Point{-1, 0}

type TwoPoint struct {
	pt  Point
	dir Point
}

// Suggested implementation for a priority queue using container/heap.

type Item struct {
	priority int
	index    int
	value    TwoPoint
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// Update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value TwoPoint, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

// End of priority queue.

func part1(grid [][]byte, mind int, maxd int) int {

	// This is a Dijkstra search.

	points := PriorityQueue{}
	heap.Push(&points, &Item{value: TwoPoint{Point{0, 0}, Point{0, 0}}})
	seen := make(map[TwoPoint]bool)
	cost := 0

	// At each step, we can go 1 and turn, or 2 and turn, or 3 and turn.
	for len(points) > 0 {
		q := heap.Pop(&points).(*Item)
		cost = q.priority
		val := q.value

		// If we hit the exit, yahoo.
		if val.pt.X == WIDTH-1 && val.pt.Y == HEIGHT-1 {
			break
		}

		// If we've been here before, bail.
		if seen[val] {
			continue
		}
		if DEBUG {
			fmt.Println("Node score=", cost, "pt=", val.pt, "dir=", val.dir)
		}
		seen[val] = true

		// Check all possible directions.  We can't go the way we were going,
		// and we can't go back the way we came.
		for _, direction := range []Point{N, E, S, W} {
			if direction == val.dir || direction == val.dir.Back() {
				continue
			}
			dcost := 0
			npt := val.pt
			for distance := 1; distance <= maxd; distance++ {
				npt = npt.Add(direction)
				if !npt.InRange(WIDTH, HEIGHT) {
					break
				}
				dcost += int(grid[npt.Y][npt.X])
				if distance >= mind {
					heap.Push(&points, &Item{
						priority: cost + dcost,
						value: TwoPoint{
							pt:  npt,
							dir: direction,
						},
					})
				}
			}
		}
	}
	return cost
}

func parse(input string) [][]byte {
	var grid [][]byte
	var row []byte
	for _, c := range input + "\n" {
		if c == '\n' {
			grid = append(grid, row)
			row = []byte{}
		} else {
			row = append(row, byte(c)-'0')
		}
	}
	return grid
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := parse(input)

	WIDTH = len(grid[0])
	HEIGHT = len(grid)

	fmt.Println("Part 1:", part1(grid, 1, 3))
	fmt.Println("Part 2:", part1(grid, 4, 10))
}
