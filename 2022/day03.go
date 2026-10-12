package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day03.txt
var live string


var test = `
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw`[1:]

type CharSet = map[rune]bool

func score(char rune) int {
	if char > 'Z' {
		return int(char-'a'+1)
	} else {
		return int(char-'A'+27)
	}
	return 0
}

func part1(data []string) int {
    prior := 0
	for _,row := range data {
        h := len(row)/2
		for _,c := range row[:h] {
			second := row[h:]
			if strings.IndexRune(second, c) >= 0 {
				prior += score(c)
				break
			}
		}
	}
    return prior
}


func part2(data []string) int {
    prior := 0
	for g := 0; g < len(data); g += 3 {
		for _,c := range data[g] {
			if strings.IndexRune(data[g], c) >= 0 &&
			   strings.IndexRune(data[g+1], c) >= 0 &&
			   strings.IndexRune(data[g+2], c) >= 0  {
				prior += score(c)
				break
		    }
		}
	}
    return prior
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}



/*
def part2(data):
    prior = 0
    counter = 2
    sect = None
    for row in data:
        if sect:
            sect.intersection_update(set(row))
        else:
            sect = set(row)

        if not counter:
            prior += score(sect)
            sect = None
            counter = 3
        counter -= 1
    return prior
*/
