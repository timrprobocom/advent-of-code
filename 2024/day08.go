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

type Point = tools.Point

func part1(spots map[byte][]Point) int {
	antinodes := make(map[Point]bool)
	for _, v := range spots {
		for i1 := 0; i1 < len(v); i1++ {
			for i2 := i1 + 1; i2 < len(v); i2++ {
				dxy := v[i2].Sub(v[i1])
				antinodes[v[i1].Sub(dxy)] = true
				antinodes[v[i2].Add(dxy)] = true
			}
		}
	}

    return tools.CountIf( tools.Keys(antinodes), func(pt Point) bool {
		return tools.Between(0, pt.X, WIDTH) && tools.Between(0, pt.Y, HEIGHT) 
	})
}

func part2(spots map[byte][]Point) int {
	antinodes := make(map[Point]bool)
	for _, v := range spots {
		for i1 := 0; i1 < len(v); i1++ {
			for i2 := i1 + 1; i2 < len(v); i2++ {
				xy0 := v[i1]
				xy1 := v[i2]
				dxy := xy1.Sub(xy0)
				for xy0.InRange(WIDTH, HEIGHT) {
					antinodes[xy0] = true
					xy0 = xy0.Sub(dxy)
				}
				for xy1.InRange(WIDTH, HEIGHT) {
					antinodes[xy1] = true
					xy1 = xy1.Add(dxy)
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
