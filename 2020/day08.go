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
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6`[1:]

var test2 = `
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6`[1:]

//go:embed day08.txt
var live string


type Instruction struct {
	opc string
	arg	int
}


func onepass( program []Instruction ) (int,bool) {
    pc := 0
    accum := 0
    seen := make([]int, len(program))
    for true {
        if pc > len(program) {
            if DEBUG {
                fmt.Println("  off", pc )
			}
            return accum, false
		}
        if pc == len(program) {
            if DEBUG {
                fmt.Println("  OK", pc, accum )
			}
            return accum, true
		}
		if seen[pc] > 0 {
			if DEBUG {
				fmt.Println("  repeat", pc )
			}
			return accum, false
		}
		seen[pc] ++
		opc := program[pc].opc
		delta := program[pc].arg

        if opc == "nop" {
            // pass
		} else if opc == "acc" {
            accum += delta
        } else if opc == "jmp" {
            pc += delta - 1
		}
        pc ++
	}
    fmt.Println("WHY?\n")
    return 0, false
}

func part1(program []Instruction) int {
	val, _ := onepass(program)
    return val
}

func part2(base []Instruction) int {
    for i := range len(base) {
        program := slices.Clone(base)
        if program[i].opc == "acc" {
            continue
		}
        if DEBUG {
            fmt.Println( "Trying", i )
		}
        if program[i].opc == "nop" {
            program[i] = Instruction{"jmp",program[i].arg}
        } else if program[i].opc == "jmp" {
            program[i] = Instruction{"nop",program[i].arg}
		}
        val,ok := onepass(program)
        if ok {
			if DEBUG {
				fmt.Println( "SUCCESS", val )
			}
            return val
		}
	}
    return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

    program := []Instruction{}
	for _,line := range data {
		opc,arg,_ := strings.Cut(line, " ")
		program = append( program, Instruction{opc, tools.StrToInt(arg)})
	}

	if DEBUG {
		fmt.Println(program)
	}

	fmt.Println("Part 1:", part1(program))
	fmt.Println("Part 2:", part2(program))
}



