package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/mowshon/iterium"

	"aoc/tools"
	_ "embed"
)

// go get github.com/mowshon/iterium@v1.0.0

var DEBUG bool = false
var TEST bool = false
var test = `
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`[1:]

//go:embed day10.txt
var live string

func parse(data []string) ([][]int, [][][]int, [][]int) {
	lights := [][]int{}
	presses := [][][]int{}
	joltage := [][]int{}
	for _, line := range data {
		parts := strings.Split(line, " ")
		ll := []int{}
		for _, c := range parts[0] {
			if c == '#' {
				ll = append(ll, 1)
			} else if c == '.' {
				ll = append(ll, 0)
			}
		}
		lights = append(lights, ll)

		joltage = append(joltage, tools.SplitIntBy(parts[len(parts)-1], ","))

		pp := [][]int{}
		for _, p := range parts[1 : len(parts)-1] {
			pp = append(pp, tools.SplitIntBy(p[1:len(p)-1], ","))
		}
		presses = append(presses, pp)
	}
	return lights, presses, joltage
}

func toggle(lights []int, switches []int) {
	for _, i := range switches {
		lights[i] = 1 - lights[i]
	}
}

func part1(lights [][]int, presses [][][]int) int {
	sum := 0
	// What would a BFS look like?
	for i := 0; i < len(lights); i++ {
		target := lights[i]
		prs := presses[i]
		found := 0
		for j := 1; j <= len(prs); j++ {
			combos, _ := iterium.Combinations(prs, j).Slice()
			for _, cx := range combos {
				mylights := tools.Repeat(0, len(target))
				for _, c := range cx {
					toggle(mylights, c)
				}
				if slices.Equal(mylights, target) {
					found = j
					break
				}
			}
			if found > 0 {
				sum += found
				break
			}
		}
	}
	return sum
}

func part2(pushes [][][]int, joltage [][]int) int {

	return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	lights, presses, joltage := parse(data)
	if DEBUG {
		fmt.Println(lights)
		fmt.Println(presses)
		fmt.Println(joltage)
	}

	fmt.Println("Part 1:", part1(lights, presses))
	fmt.Println("Part 2:", part2(presses, joltage))
}
