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
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]`[1:]

//go:embed day10.txt
var live string

var scores = map[byte]int {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

var scores2 = map[byte]int {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4,
}

func part1( data []string ) (int,int) {
    score1 := 0
    score2s := []int{}
	for _,line := range data {
        for true {
            found := false
            for _,pair := range []string{"[]","()","{}","<>"} {
                if strings.Contains(line, pair) {
                    line = strings.ReplaceAll(line, pair, "")
                    found = true
				}
			}
            if ! found {
                break
			}
		}
        l2 := strings.TrimLeft(line, "({[<")
        if len(l2) > 0 {
			// Corrupted.
            score1 += scores[l2[0]]
        } else {
			// Imcomplete.
            sc := 0
			for i := len(line)-1; i >= 0; i-- {
                sc = sc * 5 + scores2[line[i]]
			}
            score2s = append( score2s, sc )
		}
	}

    slices.Sort(score2s)
    score2 := score2s[len(score2s)/2]

    return score1, score2
}



func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

    p1,p2 := part1(data)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}


