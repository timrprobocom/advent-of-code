package main

import (
	"fmt"
	"slices"
	"strings"

	"github.com/mowshon/iterium"
	"gonum.org/v1/gonum/mat"

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

		jj := parts[len(parts)-1]
		joltage = append(joltage, tools.SplitIntBy(jj[1:len(jj)-1], ","))

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

func solve( pushes [][]int, joltage []int) int {
	// So we need a system which has one row per light, one column per buttonpush set.

	fmt.Println( "len joltage", len(joltage), "len pushes", len(pushes) )
	sysx := make([]float64, len(joltage)*len(pushes))
	jolts := make([]float64, len(joltage))
	for i, j := range joltage {
		jolts[i] = float64(j)
	}
	for i, p := range pushes {
		for _, p1 := range p {
			fmt.Println( i, p1, len(joltage) );
			sysx[p1 * len(pushes) + i] = 1.0
		}
	}
	fmt.Println( "sysx\n", sysx )
	fmt.Println( "jolts\n", jolts )

	sys := mat.NewDense( len(joltage), len(pushes), sysx )
	fmt.Println("sys\n",sys);
	equals := mat.NewDense( len(joltage), 1, jolts )
	var res mat.Dense
	fmt.Println("solve", res.Solve(sys, equals))

//	if res.Solve(sys, equals) == nil {
//		fmt.Println(res)
//	}
	fmt.Println(res)
	return 0
}

func part2(pushes [][][]int, joltage [][]int) int {
	sum := 0
	for i := range pushes {
		sum += solve( pushes[i], joltage[i] )
		break
	}
	return sum
}

func encode(ttt []int) string {
	var s string
	for _, t := range ttt {
		s = s + ('A'+t)
	}
	return s
}

func decode(ttt string) []int {
	s := []int{}
	for _, t := range ttt {
		s := append(s, t-'A')
	}
	return s
}

func patterns( coeffs [][]int ) map[string]int {
	out := make(map[string]int)
	num_buttons := len(coeffs)
	num_variables := len(coeffs[0])
	all_buttons := make([]int,num_buttons)
	for i := 0; i < num_buttons; i++ {
		all_buttons[i] = i
	}
	for pattern_len := 1; pattern_len <= num_buttons; pattern_len++ {
		combos, _ := iterium.Combinations(all_buttons, pattern_len)
		sum := make([]int,num_variables)
		for  buttons := range combos {
			for _,i := range buttons {
				for j := 0; j <= len(coeffs[i]); j++ {
					sum[j] += coeffs[i][j];
				}
			}
			pattern := encode(sum);
			out[pattern] = pattern_len
		}
	}
	return out
}

// This needs to be memoized.
func solve_single_aux( goal []int ) int {
	all := true
	for _,g := range goal {
		all := all & (g == 0)
	}
	if all {
		return 0
	}

	answer := 1000000

func solve_single( coeffs [][]int, goal []int ) int {
	pattern_costs := patterns(coeffs)
	@cache
	def solve_single_aux(goal: tuple[int, ...]) -> int:
		if all(i == 0 for i in goal): return 0
		answer = 1000000
		for pattern, pattern_cost in pattern_costs.items():
			if all(i <= j and i % 2 == j % 2 for i, j in zip(pattern, goal)):
				new_goal = tuple((j - i)//2 for i, j in zip(pattern, goal))
				answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
		return answer
	return solve_single_aux(goal)
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
