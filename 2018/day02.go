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
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab`[1:]

var test2 = `
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz`[1:]

//go:embed day02.txt
var live string


func check(s string) (int, int) {
	cnts := make(map[byte]int)
	for i := range len(s) {
		cnts[s[i]] += 1
	}

    two := 0
    three := 0
    for _,cnt := range cnts {
        if cnt == 2 {
            two ++
		}
        if cnt == 3 {
            three ++
		}
	}

    return two, three
}

func part1( data []string ) int {
    twos := 0
    threes := 0
	for _,s := range data {
        t2, t3 := check(s)
        if t2 > 0 {
			twos ++
		}
        if t3 > 0 {
			threes ++
		}
	}

    if DEBUG {
        fmt.Println( twos, threes, twos * threes )
	}
    return twos * threes
}

func compare( a, b string) (bool, string) {
    diff := 0
    result := []byte{}
	for i := range len(a) {
		if a[i] == b[i] {
			result = append(result, a[i])
		} else {
            diff ++
		}
	}
    return diff == 1, string(result)
}

func part2( data []string ) string {
	for i := range len(data) {
		for j := i+1; j < len(data); j++ {
			ok, result := compare(data[i], data[j])
			if ok {
				if DEBUG {
					fmt.Println( data[i], data[j], '\n', result )
				}
				return result
			}
		}
	}
    return ""
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    data := strings.Split(strings.TrimSpace(input),"\n")

	fmt.Println("Part 1:", part1(data))
	if TEST {
		data = strings.Split(input, "\n")
	}
	fmt.Println("Part 2:", part2(data))
}
