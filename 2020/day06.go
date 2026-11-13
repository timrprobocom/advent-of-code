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
abc

a
b
c

ab
ac

a
a
a
a

b`[1:]

//go:embed day06.txt
var live string



func part1(data []string) int {
	sum := 0
    for _,chunk := range data {
		cnt := make(map[rune]bool)
		for _,c := range chunk {
			if c != '\n' {
				cnt[c] = true
			}
		}
		sum += len(cnt)
	}
    return sum
}


func part2(data []string) int {
	sum := 0
	for _,chunk := range data {
		master := make(map[rune]int)
		lines := strings.Split(chunk, "\n") 
		for _,line := range lines {
			for _,c := range line {
				master[c] ++
			}
		}
		if DEBUG {
			fmt.Println(chunk)
			fmt.Println(master)
		}
		for _,v := range master {
			if v == len(lines) {
				sum ++
			}
		}
	}

    return sum
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	input = strings.TrimSpace(input)
	data := strings.Split(input, "\n\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}


