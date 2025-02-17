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
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7`[1:]

//go:embed day15.txt
var live string

var WIDTH = -1
var HEIGHT = -1

// H = (H+N)*17 % 256

var cache map[string]int

func dohash(s string) int {
	if cache[s] > 0 {
		return cache[s]
	}
	hash := 0
	for _,c := range s {
		hash = (hash + int(c)) * 17 % 256
	}
	cache[s] = hash
	return hash
}

func part1(data string) int {
	cache = make(map[string]int)
	sum := 0
	for _, part := range strings.Split(data, ",") {
		sum += dohash(part)
	}
    return sum
}

type Box struct {
	key string
	val int
}

func find( box []Box, s string ) int {
	for n, b := range box {
		if b.key == s {
			return n
		}
	}
	return -1
}

func part2(input string) int {
	cache = make(map[string]int)
	var boxes = make([][]Box,256)

	for _, part := range strings.Split(input, ",") {
		if strings.HasSuffix(part, "-") {
            a := part[:len(part)-1]
            box := dohash(a)
			ndx := find( boxes[box], a )
			if ndx >= 0 {
				boxes[box] = append( boxes[box][:ndx], boxes[box][ndx+1:]... )
			}
        } else {
            a,b,_ := strings.Cut( part, "=")
			val := tools.StrToInt(b)
            box := dohash(a)
			ndx := find( boxes[box], a )
			if ndx >= 0 {
				boxes[box][ndx].val = val
			} else {
				boxes[box] = append( boxes[box], Box{a,val} )
			}
		}
	}
	if DEBUG {
		fmt.Println(boxes)
	}
	sum := 0
	for i,box := range boxes {
		j := 1
		for _,b := range box {
			sum += (i+1) * j * b.val
			j++
		}
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	fmt.Println("Part 1:", part1(input))
	fmt.Println("Part 2:", part2(input))
}

