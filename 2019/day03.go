package main

import (
	"Fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83"`[1:] // == distance 159  and  610
var test2 = `
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7`[1:] // = distance 135  and  410

//go:embed day03.txt
var live string

type Point = tools.Point

var deltas = map[byte]Point{
	'R': Point{1, 0},
	'L': Point{-1, 0},
	'U': Point{0, -1},
	'D': Point{0, 1},
}

// Construct the set of all points visited on this path.

type Path = map[Point]int

func makepath(s1 string) Path {
	pt := Point{0, 0}
	dist := 0
	steps := make(Path)

	for _, move := range strings.Split(s1, ",") {
		d := deltas[move[0]]
		val := tools.StrToInt(move[1:])
		for range val {
			dist++
			pt = pt.Add(d)
			steps[pt] = dist
		}
	}
	return steps
}

func part(data []string) (int, int) {

	// Construct the paths.

	p1 := makepath(data[0])
	p2 := makepath(data[1])

	// Find the intersection.

	inx := make(map[Point]bool)
	for k, _ := range p1 {
		if p2[k] > 0 {
			inx[k] = true
		}
	}

	base := Point{0, 0}
	part1 := 99999
	part2 := 99999
	for k, _ := range inx {

		// For part 1, find the minimum distance from 0,0.

		part1 = min(part1, tools.Mandist(base, k))

		// For part 2, find the minimum total steps taken.

		if p1[k]+p2[k] < part2 {
			part2 = min(part2, p1[k]+p2[k])
		}
	}

	return part1, part2
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	part1, part2 := part(data)
	fmt.Println("Part 1:", part1)
	fmt.Println("Part 2:", part2)
}
