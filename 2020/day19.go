package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false

var test = `
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb`[1:]

//go:embed day19.txt
var live string

type Rule struct {
	letter byte
	row [][]string
}

type RuleSet = map[string]Rule

// It's not necessary to conert strings to ints.  Would it matter?

func parse( chunk []string ) RuleSet {
    rules := make(RuleSet)
    for _,line := range chunk {
        ord, rule, _ := strings.Cut(line,": ")
		row := Rule{}
		if rule[0] == '"' {
			row.letter = rule[1]
		} else {
			row.row = append(row.row, []string{} )
			for _,word := range strings.Fields(rule)  {
				idx := len(row.row)-1
				if word == "|" {
					row.row = append(row.row, []string{})
				} else {
					row.row[idx] = append(row.row[idx], word)
				}
			}
		}
		rules[ord] = row
	}
	return rules
}

// If we match the start of the string, we yield the part after
// what we matched.  If we match the whole string, we yield an empty 
// string.  If we match nothing we yield nothing.

func scan(rules RuleSet, tgt string, i string, d string) []string {
	if DEBUG {
		fmt.Println( d, "Checking", tgt, "rule", i )
	}
	out := []string{}

	if len(tgt) == 0 {
		return out
	}

    // For each set of alternatives for this rule:
	// If we've found a terminal and our target string 
	// starts with the terminal, we yield the rest of the 
	// string still to be matched.

	if rules[i].letter > 0 {
		if tgt[0] == rules[i].letter {
			out = append(out, tgt[1:])
		}
		return out
	}

	for _,option := range rules[i].row {
        // If not a terminal, then try the subparts of this alternative.
        // We start with the whole string, and as we match more parts,
        // the string in the tuple gets smaller and smaller.  If we fail,
        // the tuple goes empty.
		rems := []string{tgt}
        // For each subsequence in this alternative:
		for _,token := range option {
			nrems := []string{}
            // rems[0] keeps getting smaller as we match.
            // If we fail to match, rems becomes () and remains that way.
			for _,rem := range rems {
				for _,r := range scan(rules, rem, token, d+"+ ") {
					nrems = append( nrems, r)
				}
			}
			rems = nrems
		}

        // rems now contains the part after us, which might be empty if we
        // matched everything.  If we failed, it is empty.
        // In part 2, we can actually return multiple successes.
		if DEBUG {
			fmt.Println( d, "rems", rems )
		}
		for _,rem := range rems {
			if DEBUG {
				fmt.Println( d, tgt, i, "yield", rem )
			}
            out = append(out, rem)
		}
	}
	return out
}

func process( rules RuleSet, patterns []string) int {
    // Count only calls that yielded empty strings.  Empty tuple means
    // no match, non-empty string means there was leftover.

	sum := 0
	for _,s := range patterns {
		res := scan(rules, s, "0", "")	
		if slices.Contains( res, "" ) {
			sum ++
		}
	}
    return sum
}

func part1( data [][]string ) int {
	rules := parse(data[0])
	patterns := data[1]
	return process( rules, patterns )
}

func part2( data [][]string ) int {
	ruleset := append( data[0], "8: 42 | 42 8")
	ruleset = append( ruleset, "11: 42 31 | 42 11 31")
	rules := parse(ruleset)
	patterns := data[1]
	return process( rules, patterns )
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	d1 := strings.Split(strings.TrimSpace(input), "\n\n")
	data := [][]string{
		strings.Split(d1[0],"\n"),
		strings.Split(d1[1],"\n"),
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

