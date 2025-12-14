package main

import (
	"fmt"
	"math"
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

type Unit struct {
	lights  []int
	presses [][]int
	joltage []int
}

func parse(data []string) []Unit {
	units := make([]Unit, len(data))
	for i, line := range data {
		unit := &units[i]
		parts := strings.Split(line, " ")
		ll := []int{}
		for _, c := range parts[0] {
			if c == '#' {
				ll = append(ll, 1)
			} else if c == '.' {
				ll = append(ll, 0)
			}
		}
		unit.lights = ll

		jj := parts[len(parts)-1]
		unit.joltage = tools.SplitIntBy(jj[1:len(jj)-1], ",")

		for _, p := range parts[1 : len(parts)-1] {
			unit.presses = append(unit.presses, tools.SplitIntBy(p[1:len(p)-1], ","))
		}
	}
	return units
}

func toggle(lights []int, switches []int) {
	for _, i := range switches {
		lights[i] = 1 - lights[i]
	}
}

func part1(units []Unit) int {
	sum := 0
	// What would a BFS look like?
	for _, unit := range units {
		found := 0
		for j := 1; j <= len(unit.presses); j++ {
			combos, _ := iterium.Combinations(unit.presses, j).Slice()
			for _, cx := range combos {
				mylights := tools.Repeat(0, len(unit.lights))
				for _, c := range cx {
					toggle(mylights, c)
				}
				if slices.Equal(mylights, unit.lights) {
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

var EPSILON float64 = 1e-9

type Matrix struct {
	data         [][]float64
	rows         int
	cols         int
	dependents   []int
	independents []int
}

func from_machine(unit Unit) Matrix {
	rows := len(unit.joltage)
	cols := len(unit.presses)
	data := make([][]float64, rows)
	for i := 0; i < len(data); i++ {
		data[i] = make([]float64, cols+1)
	}
	// Add all of our buttons.
	for c, prs := range unit.presses {
		for _, p := range prs {
			if p < rows { // how could it not be?
				data[p][c] = 1.0
			}
		}
	}

	// Add the joltages in the last column.

	for r, j := range unit.joltage {
		data[r][cols] = float64(j)
	}

	m := Matrix{data, rows, cols, []int{}, []int{}}
	if DEBUG {
		fmt.Println("Before gauss\n", m)
	}
	m.gaussian_elimination()
	if DEBUG {
		fmt.Println("After gauss\n", m)
	}
	return m
}

// https://en.wikipedia.org/wiki/Gaussian_elimination
func (mat *Matrix) gaussian_elimination() {
	pivot := 0
	col := 0
	for pivot < mat.rows && col < mat.cols {
		// Find the best pivot row for this column.
		// (I think this is the largest absolute value
		maxrow := 0
		var maxv float64 = 0
		for r := pivot; r < mat.rows; r++ {
			if math.Abs(mat.data[r][col]) > maxv {
				maxrow = r
				maxv = math.Abs(mat.data[r][col])
			}
		}

		if DEBUG {
			fmt.Println( "DFS, pivot", pivot, "col", col, "max is", maxrow, maxv );
		}

		// If the best value is zero, this is a free variable.
		if maxv < EPSILON {
			mat.independents = append(mat.independents, col)
			col++
			continue
		}

		// Swap rows and mark this column as dependent.
		mat.data[pivot], mat.data[maxrow] = mat.data[maxrow], mat.data[pivot]
		mat.dependents = append(mat.dependents, col)

		// Normalize pivot row.
		pivot_value := mat.data[pivot][col]
		for c := col; c <= mat.cols; c++ {
			mat.data[pivot][c] /= pivot_value
		}
		if DEBUG {
			fmt.Println( "pivot value ", pivot_value );
		}

		// Eliminate this column in all other rows.
		for r := 0; r < mat.rows; r++ {
			if r != pivot {
				factor := mat.data[r][col]
				if math.Abs(factor) > EPSILON {
					for c := col; c <= mat.cols; c++ {
						mat.data[r][c] -= factor * mat.data[pivot][c]
					}
				}
			}
		}

		if DEBUG {
			fmt.Println( mat );
		}
		pivot++
		col++
	}

	// Any remaining columns are free variables.
	for c := col; c < mat.cols; c++ {
		mat.independents = append(mat.independents, c)
	}
}

// Check if the given values for our independent variables are valid. If so, return the total button presses.

func (mat *Matrix) valid(values []int) int {
	// We start with how many times we've pressed the free variables.
	total := tools.Sum(values)

	// Calculate dependent variable values based on independent variables.
	for row := 0; row < len(mat.dependents); row++ {
		val := mat.data[row][mat.cols]
		for i, col := range mat.independents {
			val -= mat.data[row][col] * float64(values[i])
		}

		// We need non-negative, whole numbers for a valid solution.
		if val < -EPSILON {
			return -1
		}
		rounded := math.Round(val)
		if math.Abs(val-rounded) > EPSILON {
			return -1
		}

		total += int(rounded)
	}

	return total
}

func dfs(mat Matrix, idx int, values []int, min *int, max int) {
	total := 0

	// When we've assigned all independent variables, check if it's a valid solution.
	if idx == len(mat.independents) {
		total = mat.valid(values)
		if total >= 0 {
			if total < *min {
				*min = total
			}
		}
		return
	}

	// Try different values for the current independent variable.
	total = tools.Sum(values[0:idx])
	for val := 0; val < max; val++ {
		// Optimization: If we ever go above our min, we can't possibly do better.
		if total+val >= *min {
			break
		}
		values[idx] = val
		dfs(mat, idx+1, values, min, max)
	}
}

func solve(unit Unit) int {
	matrix := from_machine(unit)

	// Now we can DFS over a much smaller solution space.

	max := 0
	for _, j := range unit.joltage {
		if j > max {
			max = j
		}
	}
	max++

	min := 999999999
	values := make([]int, len(matrix.independents))
	dfs(matrix, 0, values, &min, max)
	return min
}

func part2(units []Unit) int {
	sum := 0
	for _, unit := range units {
		sum += solve(unit)
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	units := parse(data)

	fmt.Println("Part 1:", part1(units))
	fmt.Println("Part 2:", part2(units))
}
