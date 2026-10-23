package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day16.txt
var live string

var test = `
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II`[1:]


type Valve struct {
	Name	string
	Flow	int
	Tunnel0 []string
	Tunnels []*Valve
	Open	bool
}

func makeValve( line string ) *Valve {
	v := Valve{}
	parts := strings.Fields(line)
	v.Name = parts[1]
	v.Flow = tools.StrToInt(parts[4][5:len(parts[4])-1])
	for _,p := range parts[9:] {
		v.Tunnel0 = append(v.Tunnel0, p[:2] )
	}
	return &v
}

func (v *Valve) Print() {
	fmt.Println("<valve",v.Name,"flow",v.Flow,"tunnels",v.Tunnel0,"open",v.Open,">")
}

var AA *Valve

type TimeKey struct {
	Time	int
	Name1	string
	Name2	string
}

var seen map[TimeKey]int
var maxi int

func get( seen map[TimeKey]int, name TimeKey, def int) int {
	val, ok := seen[name]
	if ok {
		return val
	}
	return def
}


func part1( valves []*Valve, t int, pos *Valve, flow [] int) int {
	sumflow := tools.Sum(flow)
	if get( seen, TimeKey{t, pos.Name, ""}, -1 ) >= sumflow {
		return max(maxi, sumflow)
	}
	seen[TimeKey{t,pos.Name,""}] = sumflow

	// If we hit the end, return a value.

	if t == 30 {
		maxi = max(maxi, sumflow)
		if DEBUG {
			fmt.Println("maximum", maxi)
		}
		return maxi
	}

	// Sum up the amount released by all the open valves.

	allopen := 0
	for _,v := range valves {
		if v.Open {
			allopen += v.Flow
		}
	}

	// If there is an unopened useful valve here, open it and
	// see what the best options are with this valve being open.
	
	if ! pos.Open && pos.Flow > 0 {
		pos.Open = true
		part1( valves, t+1, pos, append( flow, allopen+pos.Flow ))
		pos.Open = false
	}

	// For all possible moves from here, make the move and 
	// see what happens.

	for _,v := range pos.Tunnels {
		part1( valves, t+1, v, append( flow, allopen ) )
	}

    return maxi
}

func part2(valves []*Valve, t int, pos1, pos2 *Valve, flow []int) int {
	sumflow := tools.Sum(flow)
	if get( seen, TimeKey{t, pos1.Name, pos2.Name}, -1 ) >= sumflow {
		return max(maxi, sumflow)
	}
	seen[TimeKey{t,pos1.Name,pos2.Name}] = sumflow

	// If we hit the end, return a value.

	if t == 26 {
		maxi = max(maxi, sumflow)
		if DEBUG {
			fmt.Println("maximum", maxi)
		}
		return maxi
	}

	allopen := 0
	for _,v := range valves {
		if v.Open {
			allopen += v.Flow
		}
	}
    
    // If all openable valves are open, then do nothing.

    donothing := true
	for _,v := range valves {
		if !v.Open && v.Flow > 0 {
			donothing = false
			break
		}
	}
	if donothing {
		part2( valves, t+1, pos1, pos2, append(flow, allopen) )
		return maxi
	}

	if !pos1.Open && pos1.Flow > 0 {
        pos1.Open = true
        allopen += pos1.Flow
        
        if ! pos2.Open && pos2.Flow > 0 {
            pos2.Open = true
            part2( valves, t + 1, pos1, pos2, append(flow, allopen+pos2.Flow) )
            pos2.Open = false
		}
		for _,v2 := range pos2.Tunnels {
            part2( valves, t + 1, pos1, v2, append(flow, allopen) )
		}

        pos1.Open = false
    } else {
        for _,v := range pos1.Tunnels {
            if ! pos2.Open && pos2.Flow > 0 {
                pos2.Open = true
                part2( valves, t + 1, v, pos2, append(flow, allopen+pos2.Flow) )
                pos2.Open = false
			}
            for _, v2 := range pos2.Tunnels {
				part2( valves, t + 1, v, v2, append(flow, allopen) )
			}
		}
	}
    return maxi
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	valves := []*Valve{}
	valveindex := make(map[string]*Valve)
	for _,line := range strings.Split(input, "\n") {
		valve := makeValve(line)
		valves = append( valves, valve )
		valveindex[valve.Name] = valve
	}

	for _,v := range valves {
		for _,s := range v.Tunnel0 {
			v.Tunnels = append( v.Tunnels, valveindex[s] )
		}
	}

	AA = valveindex["AA"]

	maxi = 0
	seen = make(map[TimeKey]int)
	fmt.Println("Part 1:", part1(valves, 1, AA, []int{0}))

	if DEBUG {
		for _,v := range valves {
			v.Print()
		}
	}

	maxi = 0
	seen = make(map[TimeKey]int)
	fmt.Println("Part 2:", part2(valves, 1, AA, AA, []int{0}))
}
