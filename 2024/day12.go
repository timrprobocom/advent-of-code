package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE`[1:]

//go:embed day12.txt
var live string

var WIDTH = -1
var HEIGHT = -1

type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

var directions []Point

// Cutesy hint:  map[X]bool is a cute way of doing set<X>.

// We have a lot of support functions in this one.

func getregion(region map[Point]bool, xy Point) map[Point]bool {
	var queue []Point
	queue = append(queue, xy)
	found := make(map[Point]bool)
	found[xy] = true

	for len(queue) > 0 {
		xy := queue[0]
		queue = queue[1:]
		for _, dxy := range directions {
			xy0 := xy.add(dxy)
			if region[xy0] && !found[xy0] {
				found[xy0] = true
				queue = append(queue, xy0)
			}
		}
	}
	return found
}

func firstkey[T comparable, U any](mapx map[T]U) T {
	var xy T
	for xy = range mapx {
		break
	}
	return xy
}

func distinctsets(regionIn []Point) []map[Point]bool {
	region := make(map[Point]bool)
	for _, xy := range regionIn {
		region[xy] = true
	}
	var regions []map[Point]bool
	for len(region) > 0 {
		xy := firstkey(region)
		newreg := getregion(region, xy)
		regions = append(regions, newreg)
		for pt := range newreg {
			delete(region, pt)
		}
	}
	return regions
}

// Return the sum of points in the region that have a neighbor NOT in the region.

func perimeter(region map[Point]bool) int64 {
	sum := 0
	for xy, _ := range region {
		for _, dxy := range directions {
			if !region[xy.add(dxy)] {
				sum++
			}
		}
	}
	return int64(sum)
}

// Find all of the border edges.  This includes all of the sides where they border, so
// it includes and x,y and a direction.

type PointDir struct {
	pt  Point
	dir Point
}

func find_border(region map[Point]bool) map[PointDir]bool {
	border := make(map[PointDir]bool)
	for xy, _ := range region {
		for _, dxy := range directions {
			if tools.Between(0, xy.x, WIDTH) && tools.Between(0, xy.y, HEIGHT) && !region[xy.add(dxy)] {
				border[PointDir{xy, dxy}] = true
			}
		}
	}
	return border
}

// Looking in a direction perpendicular to the outside edge(s), remove any edges
// that are also on the same border.

func sides(border map[PointDir]bool) int64 {
	sides := 0
	for pair, _ := range border {
		xy := pair.pt
		dxy := pair.dir
		for _, pdxy := range []Point{Point{-dxy.y, dxy.x}, Point{dxy.y, -dxy.x}} {
			xy0 := PointDir{xy.add(pdxy), dxy}
			for border[xy0] {
				delete(border, xy0)
				xy0.pt = xy0.pt.add(pdxy)
			}
		}
		sides++
	}
	return int64(sides)
}

func part1(regions []map[Point]bool) int64 {
	var sum int64 = 0
	for _, region := range regions {
		sum += int64(len(region)) * perimeter(region)
	}
	return sum
}

func part2(regions []map[Point]bool) int64 {
	var sum int64 = 0
	for _, region := range regions {
		border := find_border(region)
		sum += int64(len(region)) * sides(border)
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := strings.Split(input, "\n")
	WIDTH = len(grid[0])
	HEIGHT = len(grid)

	if DEBUG {
		fmt.Println(grid)
	}

	directions = []Point{{-1, 0}, {0, -1}, {0, 1}, {1, 0}}

	// Process the map.  First, collect all similar cells.  Then, split letters thatn
	// have multiple distinct regions.

	stats := make(map[byte][]Point)
	for y := 0; y < HEIGHT; y++ {
		for x := 0; x < WIDTH; x++ {
			stats[grid[y][x]] = append(stats[grid[y][x]], Point{x, y})
		}
	}
	if DEBUG {
		fmt.Println(stats)
	}

	var regions []map[Point]bool
	for _, region := range stats {
		for _, s := range distinctsets(region) {
			regions = append(regions, s)
		}
	}
	if DEBUG {
		fmt.Println(regions)
	}

	fmt.Println("Part 1:", part1(regions))
	fmt.Println("Part 2:", part2(regions))
}
