package main

import (
	"fmt"
	"regexp"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc`[1:]

//go:embed day02.txt
var live string

type Data struct {
	a		int
	b		int
	target	string
	haystack	string
}

func part1(data []Data) int {
	sumx := 0
	for _,task := range data {
		c := strings.Count( task.haystack, task.target)
		if task.a <= c && c <= task.b {
			sumx ++
		}
	}
	return sumx
}

func part2(data []Data) int {
	sumx := 0
	for _,task := range data {
		if (task.haystack[task.a-1] == task.target[0]) != (task.haystack[task.b-1] == task.target[0]) {
			sumx ++
		}
	}
	return sumx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	pattern := regexp.MustCompile(`(\d+)-(\d+) (.): (.*)$`)

	data := []Data{}
	for _,line := range strings.Split(input,"\n") {
		if len(line) > 0 {
			m := pattern.FindStringSubmatch(line)
			data = append( data, Data{ tools.StrToInt(m[1]), tools.StrToInt(m[2]), m[3], m[4] } )
		}
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
