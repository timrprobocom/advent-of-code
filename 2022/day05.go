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

//go:embed day05.txt
var live string

var test = `
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2`[1:]

func part1(columns [][]byte, commands [][]int8) string {
	for _,command := range commands {
		b := command[1] - 1
		c := command[2] - 1
		for range command[0] {
			last := columns[b][len(columns[b])-1]
			columns[b] = columns[b][:len(columns[b])-1]
			columns[c] = append( columns[c], last )
		}
		if DEBUG {
			fmt.Println( columns )
		}
	}
	tails := []byte{}
	for _,col := range columns {
		if len(col) > 0 {
			tails = append(tails, col[len(col)-1] )
		}
	}
    return string(tails)
}


func part2(columns [][]byte, commands [][]int8) string {
	for _,command := range commands {
		a := int(command[0])
		b := command[1] - 1
		c := command[2] - 1
		lb := len(columns[b])
		last := columns[b][lb-a:lb]
		columns[b] = columns[b][:lb-a]
		columns[c] = append( columns[c], last... )
		if DEBUG {
			fmt.Println( columns )
		}
	}
	tails := []byte{}
	for _,col := range columns {
		if len(col) > 0 {
			tails = append(tails, col[len(col)-1] )
		}
	}
    return string(tails)
}

func clone( from [][]byte ) [][]byte {
	result := make( [][]byte, len(from) )
	for i,column := range from {
		result[i] = slices.Clone(column)
	}
	return result
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	// Find the dividing line.
	i := strings.Index( input, "\n\n" )
	half := input[:i+1]
	commands := tools.GetPosNumbers[int8](input[i+2:])

	columns := make( [][]byte, 9 )
	for _,line := range strings.Split(half, "\n") {
		if line[1] == '1' {
			break
		}
		for i := 0; i*4+1 < len(line); i++ {
			o := i*4+1
			if line[o] != ' ' {
				columns[i] = slices.Insert( columns[i], 0, line[o] )
			}
		}
	}
	if DEBUG {
		fmt.Println( columns )
		fmt.Println( commands )
	}

	fmt.Println("Part 1:", part1(clone(columns),commands))
	fmt.Println("Part 2:", part2(clone(columns),commands))
}

