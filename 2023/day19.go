package main

import (
	"fmt"
	"maps"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}`[1:]

//go:embed day19.txt
var live string

type WorkFlow struct {
	xmas string
	cmp string
	need int
	next string
}

func parseWork( block string ) (string, []WorkFlow) {
	var allwork []WorkFlow
	word := ""
	name := ""
	wu := WorkFlow{}
	for _, c := range block {
		switch c {
			default:
				word += string(c)
		    case '{':
				name = word
				word = ""
			case '<','>':
				wu.xmas = word
				wu.cmp = string(c)
				word = ""
			case ':':
				wu.need = tools.StrToInt(word)
				word = ""
			case ',', '}':
				wu.next = word
				allwork = append(allwork, wu)
				wu = WorkFlow{}
				word = ""
		}
	}
	return name, allwork
}

func parseParts( block string ) map[string]int {
	ratings := make(map[string]int)
	word := ""
	key := ""
	for _,c := range block {
		switch c {
			default:
				word += string(c)
			case '=':
				key = word
				word = ""
			case '{':
				word = ""
			case ',', '}':
				ratings[key] = tools.StrToInt(word)
				word = ""
		}
	}
	return ratings
}

func part1( parts []map[string]int, flows map[string][]WorkFlow ) int {
    sum := 0
	for _, part := range parts {
        phase := "in"
		for phase != "R" && phase != "A" {
			flow := flows[phase]
			for _, step := range flow {
				if step.need == 0 {
					phase = step.next
					break
				}
                val := part[step.xmas]
                if (step.cmp == "<" && val < step.need) || (step.cmp == ">" && val > step.need) {
                    phase = step.next
                    break
				}
			}
		}
        if phase == "A" {
			for _,v := range part {
				sum += v
			}
		}
	}
    return sum
}

type Range struct {
	lo int
	hi int
}

type Queue struct {
	phase string
	part map[string]Range
}

func part2 ( flows map[string][]WorkFlow ) int64 {
	part := map[string]Range{
		"x": Range{1,4000},
		"m": Range{1,4000},
		"a": Range{1,4000},
		"s": Range{1,4000},
	}
	pending := []Queue{Queue{"in",part}}
    var sum int64 = 0
	for len(pending) > 0 {
		pp := pending[0]
		pending = pending[1:]
   
        if pp.phase == "A" {
			var prod int64 = 1
			for _,v := range pp.part {
				prod *= int64((v.hi - v.lo + 1))
			}
			sum += prod
            continue
		}
        if pp.phase == "R" {
            continue
		}

        for _,step := range flows[pp.phase] {
            if step.need == 0 {
				pending = append( pending, Queue{step.next, pp.part})
                break
			}

            // I originally had code to check for the condition where the
            // "need" value was completely above or below the range, but
            // it turns out that never happens.  EVERY rule splits a range.

			newflow := maps.Clone(pp.part)
			oldrange := pp.part[step.xmas]
			newrange := newflow[step.xmas]
            if step.cmp == "<" {
                //  x < 400   0,399   all take the jump
                //  x < 400   200,600 200..399 take the jump 400-600 move on
                //  x < 400   500,600 all move on
                newrange.hi = step.need-1
				oldrange.lo = step.need
            } else {
                //  x > 400   0,400   all move on
                //  x > 400   200,600 200..400 move on 401-600 take the jump
                //  x > 400   500,600 all take the jump
                newrange.lo = step.need+1
                oldrange.hi = step.need
			}
			newflow[step.xmas] = newrange
			pending = append( pending, Queue{step.next, newflow})
			pp.part[step.xmas] = oldrange
		}
	}
    return sum
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    work := make(map[string][]WorkFlow)
	var parts []map[string]int

    for _, line := range strings.Split(input, "\n") {
		if len(line) == 0 {
			continue
		} else if line[0] == '{' {
			parts = append( parts, parseParts(line) )
		} else {
			name, flows := parseWork(line)
			work[name] = flows
		}
	}
	if DEBUG {
		fmt.Println(work)
		fmt.Println(parts)
	}

	fmt.Println("Part 1:", part1(parts, work))
	fmt.Println("Part 2:", part2(work))
}

