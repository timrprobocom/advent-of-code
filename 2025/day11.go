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
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out`[1:]

var test2 = `
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out`[1:]

//go:embed day11.txt
var live string

type network = map[string][]string

func parse(data []string) network {
	connx := make(network)
	for _, line := range data {
		parts := strings.Split(line, " ")
		name := parts[0][:len(parts[0])-1]
		connx[name] = parts[1:]
	}
	return connx
}

var cache map[string]int

func paths(connx network, start string, end string) int {
	val, ok := cache[start+end]
	if ok {
		return val
	}

	sum := 0
	if slices.Contains(connx[start], end) {
		sum = 1
	}
	for _, n := range connx[start] {
		sum += paths(connx, n, end)
	}
	cache[start+end] = sum
	return sum
}

func part1(data []string) int {
	connx := parse(data)
	return paths(connx, "you", "out")
}

func part2(data []string) int {
	connx := parse(data)
	return 0 +
		paths(connx, "svr", "dac")*paths(connx, "dac", "fft")*paths(connx, "fft", "out") +
		paths(connx, "svr", "fft")*paths(connx, "fft", "dac")*paths(connx, "dac", "out")
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	cache = make(map[string]int)
	fmt.Println("Part 1:", part1(data))

	if TEST {
		data = strings.Split(test2, "\n")
	}
	cache = make(map[string]int)
	fmt.Println("Part 2:", part2(data))
}
