package main

import (
	"fmt"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

const MOD = 20201227

var test = []int{5764801, 17807724}

var live = []int{10604480, 4126658}

func loop(data []int) []int {
	subj := 7
	nx := 1
	answer := []int{}
	for i := 1; true; i++ {
		nx = (nx * subj) % MOD
		if slices.Contains(data, nx) {
			answer = append(answer, i)
			answer = append(answer, nx)
			fmt.Println(i, nx)
			if len(answer) == 4 {
				break
			}
		}
	}
	return answer
}

func transform(loops int, subj int) int {
	n := 1
	for range loops {
		n = (n * subj) % MOD
	}
	return n
}

func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(test, live)

	ans := loop(input)

	fmt.Println("Part 1:", transform(ans[0], ans[3]))
	fmt.Println("Part 1:", transform(ans[2], ans[1]))
}
