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

type Point = tools.Point

var directions []Point

// Cutesy hint:  map[X]bool is a cute way of doing set<X>.

type PointSet = map[Point]bool

// We have a lot of support functions in this one.

func getregion(region PointSet, xy Point) map[Point]bool {
	var queue []Point
	queue = append(queue, xy)
	found := make(PointSet)
	found[xy] = true

	for len(queue) > 0 {
		var more []Point
		for _, xy := range queue {
			for _, dxy := range directions {
				xy0 := xy.Add(dxy)
				if region[xy0] && !found[xy0] {
					found[xy0] = true
					more = append(more, xy0)
				}
			}
		}
		queue = more
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

func distinctsets(res chan PointSet, regionIn []Point) {
	region := make(PointSet)
	for _, xy := range regionIn {
		region[xy] = true
	}
	for xy,v := range region {
		if !v { continue }
		newreg := getregion(region, xy)
		res <- newreg
		for pt := range newreg {
			region[pt] = false
		}
	}
	close(res)
}

// Return the sum of points in the region that have a neighbor NOT in the region.

func perimeter(region PointSet) int64 {
	sum := 0
	for xy, _ := range region {
		for _, dxy := range directions {
			if !region[xy.Add(dxy)] {
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

func find_border(region PointSet) map[PointDir]bool {
	border := make(map[PointDir]bool)
	for xy, _ := range region {
		for _, dxy := range directions {
			if xy.InRange(WIDTH, HEIGHT) && !region[xy.Add(dxy)] {
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
		for _, pdxy := range []Point{Point{-dxy.Y, dxy.X}, Point{dxy.Y, -dxy.X}} {
			xy0 := PointDir{xy.Add(pdxy), dxy}
			for border[xy0] {
				delete(border, xy0)
				xy0.pt = xy0.pt.Add(pdxy)
			}
		}
		sides++
	}
	return int64(sides)
}

func part1(regions []PointSet) int64 {
	var sum int64 = 0
	for _, region := range regions {
		sum += int64(len(region)) * perimeter(region)
	}
	return sum
}

func part2(regions []PointSet) int64 {
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

	var regions []PointSet
	for _, region := range stats {
		sets :=  make(chan PointSet)
		go distinctsets(sets, region)
		for s := range sets {
			regions = append(regions, s)
		}
	}
	if DEBUG {
		fmt.Println(regions)
	}

	fmt.Println("Part 1:", part1(regions))
	fmt.Println("Part 2:", part2(regions))
}
