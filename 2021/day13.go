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
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5`[1:]

//go:embed day13.txt
var live string

type Point = tools.Point

type Map = map[Point]bool

type Fold struct {
	axis 	byte
	loc 	int
}


func fold( grid Map, fold Fold ) Map {
    // So for fold x 5
    // x=6 becomes x=4
	newmap := make(Map)
	for pt,_ := range grid {
        if fold.axis == 'x' && pt.X > fold.loc {
			newmap[Point{fold.loc * 2 - pt.X, pt.Y}] = true
        } else if fold.axis == 'y' && pt.Y > fold.loc {
			newmap[Point{pt.X, fold.loc * 2 - pt.Y}] = true
        } else {
            newmap[pt] = true
		}
	}
    return newmap
}

func render( dots Map ) string {
	w := 0
	h := 0
	for pt,_ := range dots {
		w = max( w, pt.X )
		h = max( h, pt.Y )
	}
	w ++
	h ++
	layout := make( [][]byte, h )
	for i := range h {
		layout[i] = tools.Repeat[byte](' ', w)
	}
    for pt,_ := range dots {
        layout[pt.Y][pt.X] = '#'
	}
	s := ""
	for _,row := range layout {
		s += string(row) + "\n"
	}
    return s
}

func part1( dots Map, folds []Fold ) int {
    return len(fold(dots, folds[0]))
}

func part2( dots Map, folds []Fold ) string {
    for _,f := range folds {
        dots = fold( dots, f )
	}
    return "\n"+render(dots)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	dots := make(Map)
	folds := []Fold{}

	for _,row := range strings.Split(input, "\n") {
		if len(row) == 0 {
			continue
		}
		if row[0] == 'f' {
			i := strings.Index(row, "=")
			folds = append( folds, Fold{row[i-1], tools.StrToInt(row[i+1:])} )
		} else {
			i := strings.Index(row, ",")
			pt := Point{ tools.StrToInt(row[:i]), tools.StrToInt(row[i+1:]) }
			dots[pt] = true
		}
	}

    if DEBUG {
		fmt.Println(dots)
		fmt.Println(folds)
	}

	fmt.Println("Part 1:", part1(dots, folds))
	fmt.Println("Part 2:", part2(dots, folds))
}

