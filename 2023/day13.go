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
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#`[1:]

//go:embed day13.txt
var live string

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func compare_columns(chart []string, a int, b int) int {
	sum := 0
	for _, row := range chart {
		sum += boolToInt(row[a] != row[b])
	}
	return sum
}

func compare_rows(chart []string, a int, b int) int {
	sum := 0
	for i := range len(chart[a]) {
		sum += boolToInt(chart[a][i] != chart[b][i])
	}
	return sum
}

// 9 1 check 1   0 1
// 9 2 check 2   01 23
// 9 3 check 3   012 345
// 9 4 check 4   0123 4567
// 9 5 check 4   1234 5678
// 9 6 check 3   345 678
// 9 7 check 2   56 78
// 9 8 check 1   7 8

func find_h_reflect(chart []string, target int) int {
	W := len(chart[0])
	//H := len(chart)
	for col := 1; col < W; col++ {
		miss := 0
		for i := range min(col, W-col) {
			miss += compare_columns(chart, col-1-i, col+i)
		}
		if miss == target {
			if DEBUG {
				fmt.Println("H", col)
			}
			return col
		}
	}
	return 0
}

func find_v_reflect(chart []string, target int) int {
	//W := len(chart[0])
	H := len(chart)
	for row := 1; row < H; row++ {
		miss := 0
		for i := range min(row, H-row) {
			miss += compare_rows(chart, row-1-i, row+i)
		}
		if miss == target {
			if DEBUG {
				fmt.Println("V", row)
			}
			return row
		}
	}
	return 0
}

func part1(part int, data [][]string) int {
	sum := 0
	for _, chart := range data {
		h := find_h_reflect(chart, part-1)
		v := find_v_reflect(chart, part-1)
		if DEBUG {
			fmt.Println(h, v)
		}
		sum += 100*v + h
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	// Parse the input.

	charts := [][]string{}
	for _, chunk := range strings.Split(input, "\n\n") {
		charts = append(charts, strings.Fields(chunk))
	}

	fmt.Println("Part 1:", part1(1, charts))
	fmt.Println("Part 2:", part1(2, charts))
}
