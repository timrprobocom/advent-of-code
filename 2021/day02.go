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
forward 5
down 5
forward 8
up 3
down 8
forward 2`[1:]

//go:embed day02.txt
var live string


func part1(data []string) int {
	pos := 0
	depth := 0
	for _,line := range data {
		parts := strings.Fields(line)
		verb := parts[0]
		cnt := tools.StrToInt(parts[1])
		if verb == "forward" {
			pos += cnt
		} else if verb == "up" {
			depth -= cnt
		} else if verb == "down" {
			depth += cnt
		}
	}
	return pos * depth
}


func part2(data []string) int {
	pos := 0
	depth := 0
	aim := 0
	for _,line := range data {
		parts := strings.Fields(line)
		verb := parts[0]
		cnt := tools.StrToInt(parts[1])
		if verb == "forward" {
			pos += cnt
			depth += aim * cnt
		} else if verb == "up" {
			aim -= cnt
		} else if verb == "down" {
			aim += cnt
		}
	}
	return pos * depth
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
