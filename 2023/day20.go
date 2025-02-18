package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test1 = `
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a`[1:]

var test = `
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output`[1:]

//go:embed day20.txt
var live string

type Output struct {
	gate   string
	output string
	state  byte
}

// go's class/object system is half-assed.	It obviously was not in there from
// the start, and was slapped on.  There's just no way to do the kind of simple
// derived type classes that make this easy in Python.

const GATE = 0
const BROADCAST = 1
const FLIPFLOP = 2
const NAND = 3

type Gate struct {
	kind    int
	name    string
	inputs  map[string]byte
	outputs []string
	state   byte
}

func createGate(kind int, name string, outputs []string) *Gate {
	return &Gate{
		kind,
		name,
		make(map[string]byte),
		outputs,
		0,
	}
}

func (g *Gate) addinput(inp string) {
	g.inputs[inp] = 0
}

func (g *Gate) reset() {
	if g.kind == NAND {
		for k := range g.inputs {
			g.inputs[k] = 0
		}
	}
	g.state = 0
}

func (g *Gate) input(inp string, signal byte) []Output {
	switch g.kind {
	case FLIPFLOP:
		if signal > 0 {
			return []Output{}
		}
		g.state = 1 - g.state
	case NAND:
		g.inputs[inp] = signal
		g.state = 0
		for _, v := range g.inputs {
			if v == 0 {
				g.state = 1
				break
			}
		}
	}
	return g.output(g.state)
}

func (g Gate) output(state byte) []Output {
	res := []Output{}
	for _, o := range g.outputs {
		res = append(res, Output{g.name, o, g.state})
	}
	return res
}

func part1(circuit map[string]*Gate) int {
	// Push da button
	signals := []int{0, 0}

	for range 1000 {
		// Account for the button.
		signals[0] += 1
		todo := circuit["broadcaster"].output(0)
		for len(todo) > 0 {
			o := todo[0]
			todo = todo[1:]
			signals[o.state] += 1
			dst, ok := circuit[o.output]
			if ok {
				todo = append(todo, dst.input(o.gate, o.state)...)
			}
		}
	}
	if DEBUG {
		fmt.Println(signals[0], signals[1])
	}
	return signals[0] * signals[1]
}

func part2(circuit map[string]*Gate) int64 {

	// Reset the circuit.

	for _, v := range circuit {
		v.reset()
	}

	// Now we have to find the cycles.
	// rx is fed by zh in my sample, and zh is fed by sx, jt, kb, ks.
	// rx only goes LOW (the target) when zh sends a HIGH, which only
	// happens when the four inputs go LOW.  So, find the cycles.

	check := make(map[string]bool)
	first := ""
	for first = range circuit["rx"].inputs {
	}
	for o := range circuit[first].inputs {
		check[o] = true
	}

	cycles := []int64{}
	prev := make(map[string][]int)
	t := 0
	for len(cycles) < 4 {
		todo := circuit["broadcaster"].output(0)
		for len(todo) > 0 {
			o := todo[0]
			todo = todo[1:]
			if check[o.output] && o.state == 0 {
				if len(prev[o.output]) == 1 {
					cycles = append(cycles, int64(t-prev[o.output][0]))
				}
				prev[o.output] = append(prev[o.output], t)
			}
			todo = append(todo, circuit[o.output].input(o.gate, o.state)...)
		}
		t++
	}
	if DEBUG {
		fmt.Println(cycles)
		fmt.Println(prev)
	}
	return cycles[0] * cycles[1] * cycles[2] * cycles[3]
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	circuit := make(map[string]*Gate)

	for _, row := range strings.Split(input, "\n") {
		l, r, _ := strings.Cut(row, " -> ")
		right := strings.Split(r, ", ")

		if l == "broadcaster" {
			circuit[l] = createGate(BROADCAST, l, right)
		} else if l[0] == '%' {
			circuit[l[1:]] = createGate(FLIPFLOP, l[1:], right)
		} else if l[0] == '&' {
			circuit[l[1:]] = createGate(NAND, l[1:], right)
		}
	}

	circuit["rx"] = createGate(GATE, "rx", []string{})

	for name, part := range circuit {
		for _, n := range part.outputs {
			cir, ok := circuit[n]
			if ok {
				cir.addinput(name)
			}
		}
	}

	if DEBUG {
		fmt.Println(circuit)
	}

	fmt.Println("Part 1:", part1(circuit))
	if !TEST {
		fmt.Println("Part 2:", part2(circuit))
	}
}
