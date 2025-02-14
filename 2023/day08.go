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
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)`[1:]

var test2 = `
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)`[1:]

//go:embed day08.txt
var live string


func parse( data []string ) (map[string][]string, []int) {
    mapping := make(map[string][]string)
	directions := []int{}
	for _, line := range data {
        if len(line) == 0 {
            continue
		}
        if !strings.Contains(line, "=") {
			directions = tools.Repeat( 0, len(line) )
			for n,c := range line {
				if c == 'R' {
					directions[n] = 1
				}
			}
		} else {
            parts := strings.Fields(line)
			p2,_ := strings.CutPrefix(parts[2],"(")
			p2,_  = strings.CutSuffix(p2,",")
			p3,_ := strings.CutSuffix(parts[3],")")
			mapping[parts[0]] = []string{p2,p3}
		}
	}
	return mapping, directions
}

func part1 ( mapping map[string][]string, directions []int ) int {
    curr := "AAA"
	if len(mapping[curr]) == 0 {
		return -1
	}
    steps := 0
    for curr != "ZZZ" {
        i := steps % len(directions)
        curr = mapping[curr][directions[i]]
        steps ++
	}
    return steps
}

func part2 ( mapping map[string][]string, directions []int ) int64 {
    steplist := []int{}
	for g,_ := range mapping {
        if g[len(g)-1] != 'A' {
            continue
		}
        steps := 0
        for g[len(g)-1] != 'Z' {
            i := steps % len(directions)
            g = mapping[g][directions[i]]
            steps++
		}

        steplist = append(steplist, steps)
	}

    res := int64(steplist[0])
	for _,n := range steplist {
		res = tools.Lcm( res, int64(n) )
	}
    return res
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	mapping, directions := parse(data)

	fmt.Println("Part 1:", part1(mapping, directions))
	if TEST {
		data := strings.Split(test2, "\n")
		mapping, directions = parse(data)
	}
	fmt.Println("Part 2:", part2(mapping, directions))
}

