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

var directions = [][]int{
	{-1,0,0},
	{1,0,0},
	{0,-1,0},
	{0,1,0},
	{0,0,-1},
	{0,0,1},
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
			dx := row[0]+dir[0]
			dy := row[1]+dir[1]
			dz := row[2]+dir[2]
			if dx >= 0 && dy >= 0 && dz >= 0 {
				result -= box[dx][dy][dz]
			}
		}
	}
		
	return result
}


func part2( data [][]int, box [][][]int ) int {
	seen := makeEmptyBox(21)
	// This is not right.  This is NUMBER of surface cubes, not AREA.
	for x := range 20 {
		for y := range 20 {
			for z := range 20 {
				if box[x][y][z] > 0 {
					seen[x][y][z] = 1
					break
				}
			}
		}
	}
	for x := range 20 {
		for y := range 20 {
			for z := range 20 {
				if box[x][y][20-z] > 0 {
					seen[x][y][20-z] = 1
					break
				}
			}
		}
	}
	for x := range 20 {
		for z := range 20 {
			for y := range 20 {
				if box[x][y][z] > 0 && seen[x][y][z] == 0 {
					seen[x][y][z] = 1
				}
			}
		}
	}
	for x := range 20 {
		for z := range 20 {
			for y := range 20 {
				if box[x][20-y][z] > 0 && seen[x][20-y][z] == 0 {
					seen[x][20-y][z] = 1
				}
			}
		}
	}
	for y := range 20 {
		for z := range 20 {
			for x := range 20 {
				if box[x][y][z] > 0 && seen[x][y][z] == 0 {
					seen[x][y][z] = 1
				}
			}
		}
	}
	for y := range 21 {
		for z := range 21 {
			for x := range 21 {
				if box[20-x][y][z] > 0 && seen[20-x][y][z] == 0 {
					seen[20-x][y][z] = 1
				}
			}
		}
	}

	result := 0
	for x := range 21 {
		for y := range 21 {
			for z := range 21 {
				if seen[x][y][z] > 0 {
					result += 6
					for _,dir := range directions {
						dx := x+dir[0]
						dy := y+dir[1]
						dz := z+dir[2]
						if dx >= 0 && dy >= 0 && dz >= 0 {
							result -= box[dx][dy][dz]
						}
					}
				}
			}
		}
	}
	return result
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




/*
minx = min(x for x,y,z in data)
maxx = max(x for x,y,z in data)
miny = min(y for x,y,z in data)
maxy = max(y for x,y,z in data)
minz = min(z for x,y,z in data)
maxz = max(z for x,y,z in data)
xrange = range(minx,maxx+1)
yrange = range(miny,maxy+1)
zrange = range(minz,maxz+1)

# This eventually builds up a list of all cubes within the x,y,z range
# that are not surrounded by other cubes.  That should be the external 
# surface area.

def is_exterior(data,exterior,cube):
    if cube in data:
        return 0
    checked = set()
    todo = [cube]
    while todo:
        cube = todo.pop(0)
        if cube in checked:
            continue
        checked.add(cube)
        if cube in exterior:
            exterior.update( checked - data )
            return 1
        if cube[0] not in xrange or cube[1] not in yrange or cube[2] not in zrange:
            exterior.update( checked - data )
            return 1
        if cube not in data:
            for near in around(cube):
                todo.append(near)
    return 0

def part2(data):
    exterior = set()
    return sum( is_exterior(data,exterior,near) for cube in data for near in around(cube))
*/

