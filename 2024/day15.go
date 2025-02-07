package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^`[1:]

var test2 string = `
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<`[1:]

//go:embed day15.txt
var live string

var WIDTH int = -1
var HEIGHT int = -1

type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}


var directions = map[byte]Point{
	'<': Point{-1,0},
	'^': Point{0,-1},
	'>': Point{1,0},
	'v': Point{0,1},
}

type Grid = [][]byte

func printgrid( grid Grid ) {
	for _,row := range grid {
		fmt.Println(string(row))
	}
	fmt.Println()
}


// We call ourselves recursively, because when moving vertically,
// the number of cells being affected can double:
//  ...[][]...
//  ....[]....
//  .....@....

func can_we_move( grid Grid, pt Point, dir Point ) bool {
	affected := []Point{pt}
    c := grid[pt.y][pt.x]
    if dir.y != 0 {
        if c == '[' {
            affected = append(affected, pt.addi(1,0))
        } else if c == ']' {
            affected = append(affected, pt.addi(-1,0))
		}
	}

    for _, pt := range affected {
		npt := pt.add(dir)
        switch grid[npt.y][npt.x] {
		case '.':
			continue
		case '#':
			return false
		case 'O','[',']':
            if ! can_we_move(grid, npt, dir) {
                return false
			}
		}
	}
    return true
}


func do_a_move( grid Grid, pt Point, dir Point ) bool {
    if ! can_we_move(grid, pt, dir) {
        return false
	}
	affected := []Point{pt}
    c := grid[pt.y][pt.x]
    if dir.y != 0 {
        if c == '[' {
            affected = append(affected, pt.addi(1,0))
        } else if c == ']' {
            affected = append(affected, pt.addi(-1,0))
		}
	}

    for _, pt := range affected {
        c := grid[pt.y][pt.x]
		npt := pt.add(dir)
        dc := grid[npt.y][npt.x] 
		if dc == '#' {
			// Should not happen.
			printgrid(grid)
			fmt.Println(affected)
			fmt.Println(pt,npt)
			panic("Hit a brick wall")
		}
		if dc != '.' {
            do_a_move(grid, npt, dir)
		}
        grid[pt.y][pt.x] = '.'
		grid[npt.y][npt.x] = c
	}
	return true
}


func part1( moves string, grid Grid, robot Point ) int {
    if DEBUG {
        fmt.Println("START")
        printgrid(grid)
	}
	for _, c := range moves {
        dir := directions[byte(c)]
        if do_a_move(grid, robot, dir) {
			robot = robot.add(dir)
            if grid[robot.y][robot.x] != '@' {
                printgrid(grid)
                fmt.Println(robot)
				panic("Robot didn't move")
			}
		}
	}
    if DEBUG {
        printgrid(grid)
	}
    
    score := 0
    for y,row := range grid {
        for x,c := range row {
			if c == 'O' || c == '[' {
                score += y * 100 + x
			}
		}
	}
    return score
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")
	WIDTH = len(data[0])
	HEIGHT = WIDTH

    var sgrid Grid
	var dgrid Grid
	var moves string
	var srobot Point
	var drobot Point
	for y, line := range data {
		if len(line) == 0 {
			continue 
		}
		if line[0] == '#' {
			drow := ""
			for x, c := range line {
				if c == 'O' {
					drow += "[]"
				} else if c == '@' {
					drow += "@."
					srobot = Point{x,y}
					drobot = Point{x+x,y}
				} else {
					drow += string(c)+string(c)
				}
			}
			sgrid = append( sgrid, []byte(line) )
			dgrid = append( dgrid, []byte(drow) )
		} else {
			moves += line
		}
	}

    if DEBUG {
		printgrid( sgrid )
		printgrid( dgrid )
	}

	fmt.Println("Part 1:", part1(moves,sgrid,srobot))
	fmt.Println("Part 2:", part1(moves,dgrid,drobot))
}


