package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test1 = []string{
"80871224585914546619083218645595", // becomes 24176176.
"19617804207202209144916044189917", // becomes 73745418.
"69317163492948606335995924319873", // becomes 52432133.
}

var test2 = []string {
"03036732577212944063491565474664", // becomes 84462026.
"02935109699940807407585447034323", // becomes 78725270.
"03081770884921959731165446850517", // becomes 53553731.
}

var test = ""

//go:embed day16.txt
var live string

var abs = tools.AbsInt[int]

func sum(in []int8) int {
	sum := 0
	for _,n := range in {
		sum += int(n)
	}
	return sum
}

// This works for pass 1 but is way too slow for pass 2.

func onepass( digits []int8, offset int ) []int8 {
    nextx := []int8{}
	for n := range len(digits) {
        sumx := 0
        np1 := n+offset+1
		// For n=0:  0, 4, 8, 12.    0 + 4x
		// For n=1:  1, 9, 17, 25    1 + 8x
		// for n=2:  2, 14, 26, 38   2 + 12x
		for i := n; i < len(digits); i += 4*np1 {
			p1 := min(i+np1,len(digits))
			p2 := min(i+2*np1,len(digits))
			p3 := min(i+3*np1,len(digits))
            sumx += sum(digits[i:p1]) - sum(digits[p2:p3])
		}
		nextx = append(nextx, int8(abs(sumx) % 10))
	}
    return nextx
}

// This works for pass 2.
//
// This relies on the knowledge that the offset starts WAY far
// into the string.  At offset 250000, the multiply array
// will have 249999 0s, then 250000 1s, and none of them
// are longer than twice the offset.  Each succeeding line
// just excludes the next digit.

func offsetpass(digits []int8, _ int) []int8 {
    sumx := sum(digits)
	nextx := make([]int8, len(digits))
	for i,n := range digits { 
		nextx[i] = int8(sumx % 10)
        sumx += 10 - int(n)
	}
    return nextx
}

func decode( s string ) []int8 {
	out := make([]int8,len(s))
	for i := 0; i < len(s); i++ {
		out[i] = int8(s[i]-'0')
	}
	return out
}

func encode( s []int8 ) string {
	out := ""
	for i := 0; i < len(s); i++ {
		out += string("0123456789"[s[i]])
	}
	return out
}

func do100( pat string, process func([]int8,int)[]int8, rep int, ofs int) string {
	// Example: 32 10000 303673
	// So we keep 320000-303673 = 16327.
	// So repeat (16327/32 + 1) times and skip 303673 % 32 = 25
	base := decode(pat)
	if rep > 1 {
		need := (len(pat) * rep - ofs) / len(pat) + 1
		base = decode(strings.Repeat( pat, need )[ofs % len(pat):])
	}
	for range 100 {
        base = process(base,ofs)
	}
	return encode(base[:8])
}

// Part 1

func part1( data string ) string {
    return do100(data, onepass, 1, 0)
}


// Part 2.

func part2( data string ) string {
    offset := tools.StrToInt(data[:7])
    if len(data) >= 2 * offset {
		print("Assertion failed\n")
		return "-999"
	}
    return do100( data, offsetpass, 10000, offset )
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test,live)
	data := strings.TrimSpace(input)

    if TEST {
	    for _,seq := range test1 {
			fmt.Println( "Test 1:", part1(seq))
		}
		for _,seq := range test2 {
			fmt.Println( "Test 2:", part2(seq))
		}
	} else {
		fmt.Println( "Part 1:", part1(data))
		fmt.Println( "Part 2:", part2(data))
	}
}

