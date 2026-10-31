package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day21.txt
var live string


var test = `
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32`[1:]


type Knowns = map[string]int
type Unknowns = map[string][]string

var known Knowns
var unknown Unknowns

func parse( data []string ) {
    known = make(Knowns)
    unknown = make(Unknowns)
    for _,line := range data {
        parts := strings.Fields(line)
		name := parts[0][:len(parts[0])-1]
        if len(parts) == 2 {
            known[name] = tools.StrToInt(parts[1])
        } else {
            unknown[name] = parts[1:]
		}
	}
}


func lookup( name string ) int {
	val,ok := known[name]
    if ok {
        return val
	}

    part := unknown[name]
	a := part[0]
	op := part[1]
	b := part[2]

    if op == "+" {
        return lookup(a)+lookup(b)
    } else if op == "-" {
        return lookup(a)-lookup(b)
    } else if  op == "*" {
        return lookup(a)*lookup(b)
    } else if  op == "/" {
        return lookup(a)/lookup(b)
	}
	return 0
}

func part1( data []string ) int {
	parse(data)
    return lookup("root")
}


func part2( data []string ) int {
	parse(data)
	part := unknown["root"]
	left := part[0]
	right := part[2]
    R := lookup(right)
    
    base := 10000
    for true {
        known["humn"] = base
        L := lookup(left)
        if L == R {
            return base
		}
        if L > R {
            base *= 10 
        } else {
            break
		}
	}

    base /= 10
    incr := base
    for true {
        known["humn"] = base
        L := lookup(left)
        if L == R {
            break
		}
        if L > R {
            base += incr
        } else {
            base -= incr
            incr /= 10
		}
	}

    // The answer is not unique.  The next two values also work.

    for i := range 3 {
        known["humn"] = base+i
		if lookup(left) != R {
			fmt.Println("ASSERT FAILED", lookup(left), R )
		}
	}

    return base
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n") 

	fmt.Println("Part 1:", part1(data) )
	if !TEST {
		fmt.Println("Part 2:", part2(data) )
	}
}


