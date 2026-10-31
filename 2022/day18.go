package main

import (
	"fmt"
//	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day18.txt
var live string

var test = `
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5`[1:]

type Cube struct {
	X int
	Y int
	Z int
}

func (pt Cube) Add(other Cube) Cube {
	return Cube{
		pt.X + other.X,
		pt.Y + other.Y,
		pt.Z + other.Z,
	}
}


var directions = []Cube{
	Cube{-1,0,0},
	Cube{1,0,0},
	Cube{0,-1,0},
	Cube{0,1,0},
	Cube{0,0,-1},
	Cube{0,0,1},
}


func makeEmptyBox(size int) [][][]int {
    box := make([][][]int, 21)
	for i := range 21 {
		box[i] = make([][]int, 21)
		for j := range 21 {
			box[i][j] = make([]int, 21)
		}
	}
	return box
}


func part1( data [][]int, box [][][]int ) int {
	result := 0
	for _,row := range data {
		result += 6
		for _,dir := range directions {
			dx := row[0]+dir.X
			dy := row[1]+dir.Y
			dz := row[2]+dir.Z
			if dx >= 0 && dy >= 0 && dz >= 0 {
				result -= box[dx][dy][dz]
			}
		}
	}
		
	return result
}

func plot(box [][][]int) {
	for x := range 20 {
		for y := range 20 {
			fmt.Println( box[x][y] )
		}
		fmt.Println()
	}
}


func part2( data [][]int, box [][][]int ) int {

	// Do a flood fill from any corner.  This algorithm misses any
	// face with a 0 coordinate.  We should have the array start at -1,
	// but go makes that awkward.

	faces := 0
	for _,pt := range data {
		if pt[0] * pt[1] * pt[2] == 0 {
			faces ++
		}
	}

	queue := tools.Stack[Cube]{}
	queue.Push(Cube{0,0,0})
    seen := makeEmptyBox(21)
	seen[0][0][0] = 1
	
	for !queue.IsEmpty() {
		point,_ := queue.Pop()
		seen[point.X][point.Y][point.Z] = 1
		for _,dir := range directions {
			pt := point.Add(dir)
			if !tools.Between(0,pt.X,21) || !tools.Between(0,pt.Y,21) || !tools.Between(0,pt.Z,21) || seen[pt.X][pt.Y][pt.Z] > 0 {
				continue
			}
			if box[pt.X][pt.Y][pt.Z] > 0 {
				faces ++
			} else {
				if pt.X >= 0 && pt.Y >= 0 && pt.Z >= 0 {
				seen[pt.X][pt.Y][pt.Z] = 1
				}
				queue.Push(pt)
			}
		}
	}
	return faces
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := tools.GetNumbers[int](input)

    box := makeEmptyBox(21)

	for _,row := range data {
		box[row[0]][row[1]][row[2]] = 1
	}

	fmt.Println("Part 1:", part1(data, box) )
	fmt.Println("Part 2:", part2(data, box) )
}
