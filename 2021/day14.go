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
NNCB

BB -> N
BC -> B
BH -> H
BN -> B
CB -> H
CC -> N
CH -> B
CN -> C
HB -> C
HC -> B
HH -> N
HN -> C
NB -> B
NC -> B
NH -> C
NN -> C`[1:]

//go:embed day14.txt
var live string

type Counter = map[string]int

func concat(a, b byte) string {
	return string(a)+string(b)
}

func generation( counts Counter, xform map[string]byte ) Counter {
    newcounts := make(Counter)
    for k,v := range xform {
        newcounts[concat(k[0],v)] += counts[k]
        newcounts[concat(v,k[1])] += counts[k]
	}
    return newcounts
}


func part1( polymer string, xform map[string]byte, gems int ) int {
    counts := make(Counter)
	for i := 0; i < len(polymer)-1; i++ {
		a := polymer[i]
		b := polymer[i+1]
		counts[concat(a,b)] ++
	}
    for _ = range gems {
        counts = generation(counts, xform)
	}

    counter := make(map[byte]int)
    counter[polymer[0]] = 1
    counter[polymer[len(polymer)-1]] = 1
    for k,v := range counts {
        counter[k[0]] += v
        counter[k[1]] += v
	}
        
    a := tools.Max(tools.Values(counter))/2
    b := tools.Min(tools.Values(counter))/2
    return a-b
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	polymer := data[0]
	xform := make(map[string]byte)

    for _,row := range data[2:] {
		xform[row[0:2]] = row[6]
	}

	fmt.Println("Part 1:", part1(polymer, xform, 10))
	fmt.Println("Part 2:", part1(polymer, xform, 40))
}

