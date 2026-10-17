package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day06.txt
var live string

var test = `
mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw`[1:]

func unique( s string ) bool {
	counts := make([]int, 26)
	for i := 0; i < len(s); i++ {
		if counts[s[i]-97] > 0 {
			return false
		}
		counts[s[i]-97] += 1
	}
	return true
}

func part1(data string, target int) int {
	for i := target; i < len(data); i++ {
		if unique( data[i-target: i] ) {
			return i
		}
	}
    return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split( input, "\n" )

	for _,line := range data {
		fmt.Println("Part 1:", part1(line,4))
	}
	for _,line := range data {
		fmt.Println("Part 2:", part1(line,14))
	}
}
