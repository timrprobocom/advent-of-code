package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day08.txt
var live string

var test = `
30373
25512
65332
33549
35390`[1:]

// Make a visibility matrix.

func visibility(data []string) [][]int8 {
	h := len(data)
	w := len(data[0])
	vis := make([][]int8, h)
	for yy := range h {
		vis[yy] = make([]int8, w)
		vis[yy][0] = 1
		vis[yy][w-1] = 1
	}
	for xx := range w {
		vis[0][xx] = 1
		vis[h-1][xx] = 1
	}

	// Scan each row.

	for yy := 1; yy < h-1; yy++ {
		ll := data[yy][0]
		rr := data[yy][w-1]
		for xx := 1; xx < w-1; xx++ {
			if data[yy][xx] > ll {
				vis[yy][xx] = 1
				ll = data[yy][xx]
			}
			if data[yy][w-xx-1] > rr {
				vis[yy][w-xx-1] = 1
				rr = data[yy][w-xx-1]
			}
		}
	}

	// Scan each column.

	for xx := 1; xx < w-1; xx++ {
		ll := data[0][xx]
		rr := data[h-1][xx]
		for yy := 1; yy < h-1; yy++ {
			if data[yy][xx] > ll {
				vis[yy][xx] = 1
				ll = data[yy][xx]
			}
			if data[h-yy-1][xx] > rr {
				vis[h-yy-1][xx] = 1
				rr = data[h-yy-1][xx]
			}
		}
	}

	return vis
}

func part1(data []string) int {
	vis := visibility(data)
	sum := 0
	for _, row := range vis {
		sum += int(tools.Sum(row))
	}
	return sum
}

func part2(data []string) int {
	h := len(data)
	w := len(data[0])
	vis := make([][]int8, h)
	for yy := range h {
		vis[yy] = make([]int8, w)
		vis[yy][0] = 1
		vis[yy][w-1] = 1
	}
	for xx := range w {
		vis[0][xx] = 1
		vis[h-1][xx] = 1
	}

	dirs := [][]int{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}
	maxx := 1

	for yy := range h {
		for xx := range w {
			mult := 1
			// In each direction:
			for _, dydx := range dirs {
				dy := dydx[0]
				dx := dydx[1]
				x0 := xx
				y0 := yy
				delta := 0
				for {
					x0 += dx
					y0 += dy
					if x0 < 0 || x0 >= w || y0 < 0 || y0 >= h {
						break
					}
					delta += 1
					if data[y0][x0] >= data[yy][xx] {
						break
					}
				}
				mult *= delta
			}
			maxx = max(maxx, mult)
		}
	}

	return maxx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

/*
def part2(data):

    dirs = ((-1,0),(1,0),(0,-1),(0,1))

    maxx = 1
    for y in range(h):
        for x in range(w):
            mult = 1
            # In each direction:
            for dy,dx in dirs:
                x0,y0,delta = x,y,0
                while True:
                    x0 += dx
                    y0 += dy
                    if not x0 in range(w) or not y0 in range(h):
                        break
                    delta += 1
                    if data[y0][x0] >= data[y][x]:
                        break
                mult *= delta
            maxx = max(maxx,mult)
    return maxx
*/
