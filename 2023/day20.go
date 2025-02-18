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
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a`[1:]

var test2 = `
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output`[1:]

//go:embed day20.txt
var live string


type Output struct {
	gate Gate
	output string
	state bool
}


type Gate interface {
    addinput(inp string)
	reset()
	input(inp string, signal bool) []Output
	output(state bool) []Output
}

type Broadcast struct {
	name string
	inputs map[string]bool
	outputs []string
	state bool
}

type FlipFlop struct {
	name string
	inputs map[string]bool
	outputs []string
	state bool
}

type Nand struct {
	name string
	inputs map[string]bool
	outputs []string
	state bool
}

// Broadcast.

func createBroadcast( name string, outputs []string ) Broadcast {
	return Broadcast{
		name,
		make(map[string]bool),
		outputs,
		false,
	}
}

func (g Broadcast) addinput( inp string ) {
	g.inputs[inp] = false
}

func (g Broadcast) reset() {
	g.state = false
}

func (g Broadcast) input( inp string, signal bool ) []Output {
	return g.output(false)
}

func (g Broadcast) output( state bool ) []Output {
	res := []Output{}
	for _, o := range g.outputs {
		res = append( res, Output{ g, o, g.state } )
	}
    return res
}

// FlipFlop.

func createFlipFlop( name string, outputs []string ) FlipFlop {
	return FlipFlop{
		name,
		make(map[string]bool),
		outputs,
		false,
	}
}

func (g FlipFlop) addinput( inp string ) {
	g.inputs[inp] = false
}

func (g FlipFlop) reset() {
	g.state = false
}

func (g FlipFlop) input( inp string, signal bool ) []Output {
    if signal {
		g.state = !g.state
		return g.output(g.state)
	}
	return []Output{}
}

func (g FlipFlop) output( state bool ) []Output {
	res := []Output{}
	for _, o := range g.outputs {
		res = append( res, Output{ g, o, g.state } )
	}
    return res
}

// Nand.

func createNand( name string, outputs []string ) Nand {
	return Nand{
		name,
		make(map[string]bool),
		outputs,
		false,
	}
}

func (g Nand) addinput( inp string ) {
	g.inputs[inp] = false
}

func (g Nand) reset() {
	for k := range g.inputs {
		g.inputs[k] = false
	}
}

func (g Nand) input( inp string, signal bool ) []Output {
	g.inputs[inp] = signal
	for _, v := range g.inputs {
		if !v {
			return g.output(true)
		}
	}
	return g.output(false)
}

func (g Nand) output( state bool ) []Output {
	res := []Output{}
	for _, o := range g.outputs {
		res = append( res, Output{ g, o, g.state } )
	}
    return res
}

	
func part1 ( circuit map[string]Output ) int {
    // Push da button
	signals := []int{0,0}
    
	for range 1000 {
        // Account for the button.
        signals[0] += 1
        todo := circuit["broadcaster"].input()
        for len(todo) > 0 {
			o := todo[0]
			todo = todo[1:]
            signals[o.state] += 1
			dst, ok := circuit[o.dst]
            if ok {
				todo = append( todo, dst.gate.input(o.src.name, o.state)... )
			}
		}
	}
    if DEBUG {
        fmt.Println(signals[0],signals[1])
	}
    return signals[0]*signals[1]
}




func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	circuit := make(map[string]Gate)

	for _, row := range strings.Split(input, "\n") {
		l,r,_ := strings.Cut(row ," -> ")
		right := strings.Split(r, ", ")

		if l == "broadcaster" {
			circuit[l] = createBroadcast(l,right)
		} else if l[0] == '%' {
			circuit[l[1:]] = createFlipFlop(l[1:],right)
		} else if l[0] == '&' {
			circuit[l[1:]] = createNand(l[1:],right)
		}
	}

//	circuit["rx"] = Part("rx",[])
	circuit["rx"] = createBroadcast("rx",[]string{})

	for name,part := range circuit {
		for _, n := range part.outputs {	// I neet Gate.Output to return outputs.
			cir, ok := circuit[n]
			if ok {
				cir.addinput(name)
			}
		}
	}

	fmt.Println("Part 1:", part1(circuit))
	if !TEST {
//		fmt.Println("Part 2:", part2(circuit))
	}
}


/*
def part2(circuit):

    # Reset the circuit.

    for p in circuit.values():
        if not isinstance(p,int):
            p.reset()

    # Now we have to find the cycles.
    # rx is fed by zh in my sample, and zh is fed by sx, jt, kb, ks.
    # rx only goes LOW (the target) when zh sends a HIGH, which only
    # happens when the four inputs go LOW.  So, find the cycles.

    check = list(circuit[list(circuit['rx'].inputs)[0]].inputs)
    if DEBUG:
        print(check)
    cycles = []
    prev = collections.defaultdict(list)
    t = 0
    while len(cycles) < 4:
        todo = circuit['broadcaster'].input()
        while todo:
            src,dst,state = todo.pop(0)                
            if dst in check and not state:
                if len(prev[dst]) == 1:
                    cycles.append( t - prev[dst][0] )
                prev[dst].append( t )
            todo.extend( circuit[dst].input(src.name, state))
        t += 1
    if DEBUG:
        print(cycles)
        print(prev)
    return math.prod(cycles)
	*/
