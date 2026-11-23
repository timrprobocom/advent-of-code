package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = [][]int{
	{109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99}, //# takes no input and produces a copy of itself as output.
	{1102,34915192,34915192,7,4,7,99,0}, //# should output a 16-digit number.
	{104,1125899906842624,99}, // should output the large number in the middle.
}

//go:embed day09.txt
var live string


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup("", live)
	if TEST {
		for _,p := range test {
			fmt.Println( "Part 1:", tools.MakeProgram(p).Run().Dump())
		}
	} else {
		data := tools.GetRowNumbers[int](input)

		pgm := tools.MakeProgram(data)
		pgm.Push(1)
		fmt.Println( "Part 1:", pgm.Run().Dump()[0] )

		pgm = tools.MakeProgram(data)
		pgm.Push(2)
		fmt.Println( "Part 2:", pgm.Run().Dump()[0] )
	}
}

