package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689`[1:]

//go:embed day08.txt
var live string

func dist3d(a []int, b []int) int {
	return (b[0]-a[0])*(b[0]-a[0]) + (b[1]-a[1])*(b[1]-a[1]) + (b[2]-a[2])*(b[2]-a[2])
}

type Dist struct {
	dist int
	a    int
	b    int
}

func hash(pts []int) int {
	return ((pts[0]*100000)+pts[1])*100000 + pts[2]
}

func getCounts(circuits []int) map[int]int {
	counts := make(map[int]int)
	for _, c := range circuits {
		counts[c]++
	}
	return counts
}

func part1(data [][]int, dists []Dist) int {
	// We assign each junction to a circuit.
	circuit := make(map[int]int)
	for i, j := range data {
		circuit[hash(j)] = i
	}

	limit := 1000
	if TEST {
		limit = 10
	}

	for _, d := range dists[:limit] {
		bindex := circuit[d.b]
		for c := range circuit {
			if circuit[c] == bindex {
				circuit[c] = circuit[d.a]
			}
		}
	}

	// Find the 3 most common.

	counts := getCounts(tools.Values(circuit))
	countx := tools.Values(counts)
	slices.Sort(countx)
	slices.Reverse(countx)
	return countx[0] * countx[1] * countx[2]
}

func part2(data [][]int, dists []Dist) int {
	// We assign each junction to a circuit.

	circuit := make(map[int]int)
	for i, j := range data {
		circuit[hash(j)] = i
	}

	for _, d := range dists {
		bindex := circuit[d.b]
		for c := range circuit {
			if circuit[c] == bindex {
				circuit[c] = circuit[d.a]
			}
		}
		if len(getCounts(tools.Values(circuit))) == 1 {
			return (d.a / 10000000000) * (d.b / 10000000000)
		}
	}

	return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := [][]int{}
	for _, row := range strings.Split(input, "\n") {
		p := strings.Split(row, ",")
		data = append(data, []int{
			tools.StrToInt(p[0]),
			tools.StrToInt(p[1]),
			tools.StrToInt(p[2])})
	}

	distances := []Dist{}
	for i, a := range data {
		for _, b := range data[i+1:] {
			distances = append(distances, Dist{dist3d(a, b), hash(a), hash(b)})
		}
	}
	slices.SortFunc(distances, func(a Dist, b Dist) int { return a.dist - b.dist })

	fmt.Println("Part 1:", part1(data, distances))
	fmt.Println("Part 2:", part2(data, distances))
}
