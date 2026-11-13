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
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.`[1:]

var test2 = `
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.`[1:]

//go:embed day07.txt
var live string


type Rule struct {
	count int
	bag string
}

type RuleSet = map[string][]Rule

// Does this bag contain the target?

func descend( rules RuleSet, bag string, target string ) bool {
	if bag == target {
		return true
	}

	for _,b := range rules[bag] {
		if descend( rules, b.bag, target ) {
			return true 
		}
	}

	return false
}

func part1(target string, rules RuleSet) int {
	sum := 0
	for key,_ := range rules {
		if key != target && descend(rules,key,target) {
			sum ++
		}
	}

    return sum
}

// How many bags would this bag contain, not counting itself?

func contains( rules RuleSet, target string ) int {
	sum := 0
	for _,v := range rules[target] {
		sum += v.count * (contains(rules, v.bag) + 1)
	}
    return sum
}

func part2(target string, rules RuleSet) int {
    return contains( rules, target )
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

    rules := make(RuleSet)
	for _,ln := range data {
		left, right, _ := strings.Cut(ln, " bags contain ")
		rules[left] = []Rule{}
		if right != "no other bags." {
			for _,part := range strings.Split(right, ", ") {
				words := strings.Fields(part)
				count := tools.StrToInt(words[0])
				rules[left] = append(rules[left], Rule{count,words[1]+" "+words[2]})
			}
		}
	}

	if DEBUG {
		fmt.Println(rules)
	}

    target := "shiny gold"

	fmt.Println("Part 1:", part1(target, rules))
	fmt.Println("Part 2:", part2(target, rules))
}



