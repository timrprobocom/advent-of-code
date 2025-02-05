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
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`[1:]

//go:embed day08.txt
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

func part1(spots map[byte][]Point) int {
	antinodes := make(map[Point]bool)
	for _, v := range spots {
		for i1 := 0; i1 < len(v); i1++ {
			for i2 := i1 + 1; i2 < len(v); i2++ {
				dxy := v[i2].sub(v[i1])
				antinodes[v[i1].sub(dxy)] = true
				antinodes[v[i2].add(dxy)] = true
			}
		}
	}

	sum := 0
	for pt := range antinodes {
		if tools.Between(0, pt.x, WIDTH) && tools.Between(0, pt.y, HEIGHT) {
			sum++
		}
	}
	return sum
}

func part2(spots map[byte][]Point) int {
	antinodes := make(map[Point]bool)
	for _, v := range spots {
		for i1 := 0; i1 < len(v); i1++ {
			for i2 := i1 + 1; i2 < len(v); i2++ {
				xy0 := v[i1]
				xy1 := v[i2]
				dxy := xy1.sub(xy0)
				for tools.Between(0, xy0.x, WIDTH) && tools.Between(0, xy0.y, HEIGHT) {
					antinodes[xy0] = true
					xy0 = xy0.sub(dxy)
				}
				for tools.Between(0, xy1.x, WIDTH) && tools.Between(0, xy1.y, HEIGHT) {
					antinodes[xy1] = true
					xy1 = xy1.add(dxy)
				}
			}
		}
	}

	return len(antinodes)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	WIDTH = len(data[0])
	HEIGHT = len(data)

	spots := make(map[byte][]Point)
	for y := 0; y < HEIGHT; y++ {
		for x := 0; x < WIDTH; x++ {
			if data[y][x] != '.' {
				spots[data[y][x]] = append(spots[data[y][x]], Point{x, y})
			}
		}
	}

	fmt.Println("Part 1:", part1(spots))
	fmt.Println("Part 2:", part2(spots))
}
