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
F10
N3
F7
R90
F11`[1:]

//go:embed day12.txt
var live string

type Point = tools.Point


var deltas = map[byte]Point { 
    'N': Point{ 0,-1},
    'E': Point{ 1, 0},
    'S': Point{ 0, 1},
    'W': Point{-1, 0},
}

// N and W are negative.


func part1(data []string) int {
    ship := Point{0,0}
    facing := deltas['E']
	for _,ln := range data {
        direc := ln[0]
        dist := tools.StrToInt(ln[1:])
		switch direc {
			case 'N','E','S','W':
				ship = ship.Add(deltas[direc].ScaleBy(dist))
			case 'L':
				for range dist/90 {
					facing = facing.Left()
				}
			case 'R':
				for range dist/90 {
					facing = facing.Right()
				}
			case 'F':
				ship = ship.Add(facing.ScaleBy(dist))
		}
        if DEBUG {
            fmt.Println(ln,ship)
		}
	}
	return tools.Mandist(ship, Point{0,0})
}


func part2(data []string) int {
    ship := Point{0,0}
    waypt := Point{10,-1}
    for _,ln := range data {
        direc := ln[0]
        dist := tools.StrToInt(ln[1:])
		switch direc {
			case 'N','E','W','S':
				waypt = waypt.Add(deltas[direc].ScaleBy(dist))
            case 'L':
				for range dist/90 {
					waypt = waypt.Left()
				}
            case 'R':
				for range dist/90 {
					waypt = waypt.Right()
				}
            case 'F':
				ship = ship.Add(waypt.ScaleBy(dist))
		}
        if DEBUG {
            fmt.Println(ln,ship,waypt)
		}
	}
	return tools.Mandist(ship, Point{0,0})
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(strings.TrimSpace(input), "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
