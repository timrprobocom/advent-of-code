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

//go:embed day13.txt
var live string

var test = `
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]`[1:]

// Can I do this all as strings?
// Given a pointer to each, I need an "extract next thing".
// If both are digit, compare the digits.
// If left is [, convert right to [right] and compare.
// If right is ], convert left to [left] and compare.
// Need to handle 11 vs 2.

type Track struct {
	S string
	P int
}

func (t Track) Peek() byte {
	return t.S[t.P]
}

func (t Track) IsDigit() bool {
	return tools.Isdigit(t.S[t.P])
}

func (t *Track) Next() {
	if tools.Isdigit(t.S[t.P]) {
		t.P++
	}
	t.P++
}

func (t Track) Len() int {
	return len(t.S)
}

func (t Track) Print() {
	if DEBUG {
		fmt.Println( t.S )
		fmt.Print( strings.Repeat(" ", t.P) )
		fmt.Println( "^" )
	}
}

func (t *Track) Token() *Track {
	if t.P == 0 {
		t.Next()
	}
	if t.P == len(t.S) || t.Peek() == ']' {
		return &Track{"",0}
	}
	start := t.P;
	if t.Peek() == '[' {
		t.Next()
		nest := 1
		for nest > 0 {
			if t.Peek() == '[' {
				nest ++
			} else if t.Peek() == ']' {
				nest --
			}
			t.Next()
		}
		return &Track{t.S[start:t.P],0}
	} else {
		for t.IsDigit() {
			t.Next()
		}
		end := t.P
		if t.Peek() == ',' {
			t.Next()
		}
		return &Track{"["+t.S[start:end]+"]",0}
	}
	return &Track{"",0}
}

func cmp(s, t string) int {
	s = s[:len(s)-1]
	t = t[:len(t)-1]
	if s < t {
		return -1
	} else if s > t {
		return 1
	}
	return 0
}

func compare(s, t Track) int {
	if s.S == t.S {
		if DEBUG {
			fmt.Println(s.S,"and",t.S,"compare equal")
		}
		return 0
	}

	// If there are commas, call recursively.  Otherwise, compare as strings.

	lc := strings.Count( s.S, "[" )
	rc := strings.Count( t.S, "[" )

	if lc == 1 && rc == 1 {
		i := cmp(s.S, t.S)
		if DEBUG {
			fmt.Println(s.S,"and",t.S,"no commas -- returning",i)
		}
		return cmp(s.S, t.S)
	}

	for true {
		l := s.Token()
		r := t.Token()
		if l.Len() == 0 {
			if r.Len() == 0 {
				break
			}
			if DEBUG {
				fmt.Println(s.S,"left ended first")
			}
			return -1
		}
		if r.Len() == 0 {
			if DEBUG {
				fmt.Println(t.S,"right ended first")
			}
			return 1
		}
		res := compare(*l, *r)
		if res != 0 {
			return res
		}
	}

	if DEBUG {
		fmt.Println(s.S,"and",t.S,"compared equal at end")
	}
	return 0
}

func expand(s string) string {
	// Convert all 1 digit numbers to 2 digit.

	var b strings.Builder
	for i := 0; i < len(s); i++ {
		if tools.Isdigit(s[i]) {
			if tools.Isdigit(s[i+1]) {
				b.WriteByte(s[i])
				b.WriteByte(s[i]+1)
				i++
			} else {
				b.WriteByte('0')
				b.WriteByte(s[i])
			}
		} else {
			b.WriteByte(s[i])
		}
	}
	return b.String()
}



func part1(pairs []string) int {
	sum := 0
	for i,pair := range pairs {
		p := strings.Split(pair, "\n")
		left := Track{expand(p[0]),0}
		right := Track{expand(p[1]),0}
		if DEBUG {
			left.Print()
			right.Print()
		}
		if compare(left,right) <= 0 {
			sum += i+1
		}
	}
	return sum
}

func part2(pairs []string) int {
	t1 := Track{"[[02]]",1}
	t2 := Track{"[[06]]",1}
	combine := []Track{ t1, t2 }
	for _,pair := range pairs {
		p := strings.Split(pair, "\n")
		combine = append( combine, Track{expand(p[0]),1} )
		combine = append( combine, Track{expand(p[1]),1} )
	}

	slices.SortFunc( combine, compare )
	mult := 1
	for i,row := range combine {
		row.Print()
		if row == t1 || row == t2 {
			mult *= i+1
		}
	}
	return mult
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	pairs := strings.Split(input, "\n\n")

	fmt.Println("Part 1:", part1(pairs))
	fmt.Println("Part 2:", part2(pairs))
}

