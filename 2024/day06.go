package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`[1:]

//go:embed day06.txt
var live string

var WIDTH int = -1
var HEIGHT int = -1

type Point = tools.Point

var NORTH Point = Point{0, -1}
var EAST Point = Point{-1, 0}
var SOUTH Point = Point{0, 1}
var WEST Point = Point{1, 0}

var GUARD Point = Point{-1, -1}

type Cell struct {
	walkId  int
	blocked bool
	walked  map[Point]bool
}

func (c *Cell) maybeResetCell(newwalk int) {
	if c.walkId != newwalk {
		c.walkId = newwalk
		c.walked[NORTH] = false
		c.walked[EAST] = false
		c.walked[SOUTH] = false
		c.walked[WEST] = false
	}
}

func makeCell() Cell {
	c := Cell{-1, false, make(map[Point]bool, 0)}
	c.maybeResetCell(0)
	return c
}

func parseInput(data []string) [][]Cell {
	WIDTH = len(data[0])
	HEIGHT = len(data)

	grid := make([][]Cell, HEIGHT)
	for y := 0; y < HEIGHT; y++ {
		grid[y] = make([]Cell, WIDTH)
		for x := 0; x < WIDTH; x++ {
			grid[y][x] = makeCell()
			var c = data[y][x]
			if c == '#' {
				grid[y][x].blocked = true
			} else if c == '^' {
				GUARD = Point{x, y}
			}
		}
	}
	return grid
}

// A path step includes both a coordinate and a direction.

type Step struct {
	pt  Point
	dir Point
}

// Ugliness warning -- this gets passed from pass 1 to pass 2.

var g_originalPath []Step

func part1(grid [][]Cell) int {
	gpt := GUARD
	dir := NORTH

	g_originalPath = make([]Step, 0)

	for {
		g_originalPath = append(g_originalPath, Step{gpt, dir})
		npt := gpt.Add(dir)
		if !npt.InRange(WIDTH, HEIGHT) {
			break
		}
		if grid[npt.Y][npt.X].blocked {
			dir = dir.Right()
		} else {
			gpt = npt
		}
	}

	// Count the unique cells in the path.

	visited := make(map[Point]bool)
	for _, pth := range g_originalPath {
		visited[pth.pt] = true
	}

	return len(visited)
}

var currentWalk int = 0

func walkCandidateMap(grid [][]Cell, point Step) int {
	currentWalk++
	pt := point.pt
	direction := point.dir

	for {
		// We keep walking until we get blocked.
		npt := pt.Add(direction)
		if !npt.InRange(WIDTH, HEIGHT) {
			break
		}
		if !grid[npt.Y][npt.X].blocked {
			pt = npt
			continue
		}
		currentCell := &grid[pt.Y][pt.X]
		currentCell.maybeResetCell(currentWalk)
		if currentCell.walked[direction] {
			return 1
		}
		currentCell.walked[direction] = true
		direction = direction.Right()
	}
	return 0
}

func part2(grid [][]Cell) int {
	checked := make(map[Point]bool)
	checked[GUARD] = true
	countOfLoopPaths := 0
	point := g_originalPath[0]
	for _, step := range g_originalPath {
		if step != point {
			block := step.pt
			if !checked[block] {
				checked[block] = true
				grid[block.Y][block.X].blocked = true
				countOfLoopPaths += walkCandidateMap(grid, point)
				grid[block.Y][block.X].blocked = false
			}
		}
		point = step
	}

	return countOfLoopPaths
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := parseInput(strings.Split(input, "\n"))

	fmt.Println("Part 1:", part1(grid))
	fmt.Println("Part 2:", part2(grid))
}
