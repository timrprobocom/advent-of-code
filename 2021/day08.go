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
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce`[1:]

//go:embed day08.txt
var live string

func sortString( s string ) string {
	runes := []rune(s)
	slices.Sort(runes)
	return string(runes)
}

func issubset( haystack, needle string ) bool {
	for _,c := range needle {
		if ! strings.ContainsRune(haystack, c) {
			return false
		}
	}
	return true 
}

func part1( data [][]string ) int {
	lengths := make(map[int]int)
    for _,row := range data {
        for _,word := range row[len(row)-4:] {
            lengths[len(word)] += 1
		}
	}
    return lengths[2]+lengths[3]+lengths[4]+lengths[7]
}

func part2( data [][]string ) int {
    sumall := 0
	for _,row := range data {
		i := slices.Index(row, "|" )

		p1 := []string{}
		p2 := []string{}
		for _,c := range row[:i] {
			p1 = append( p1, sortString(c))
		}
		for _,c := range row[i+1:] {
			p2 = append( p2, sortString(c))
		}

		codes := make([]string, 10)

        // Find the easy ones.

        for _,c := range p1 {
            if len(c) == 2 {
                codes[1] = c
            } else if len(c) == 3 {
                codes[7] = c
            } else if len(c) == 4 {
                codes[4] = c
            } else if len(c) == 7 {
                codes[8] = c
			}
		}

        // Now classify the 6s (0, 6, 9).

        for _,c := range p1 {
            if len(c) == 6 {
				if ! issubset(c, codes[1]) {
                    codes[6] = c
				} else if issubset(c, codes[4]) {
                    codes[9] = c
                } else {
                    codes[0] = c
				}
			}
		}

        // Now classify the 5s (2, 3, 5).

        for _,c := range p1 {
            if len(c) == 5 {
                if issubset(codes[6], c) {
                    codes[5] = c
                } else if issubset(c, codes[1]) {
                    codes[3] = c
                } else {
                    codes[2] = c
				}
			}
		}

        sumn := 0
        for _,digit := range p2 {
			if slices.Index(codes,digit) < 0 {
				fmt.Println("failed to find",digit)
			}
            sumn = sumn * 10 + slices.Index(codes, digit)
		}
        if DEBUG {
            print(sumn)
		}
        sumall += sumn
	}
    return sumall
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := [][]string{}
	for _,row := range strings.Split(input,"\n") {
		data = append( data, strings.Fields(row) )
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}


