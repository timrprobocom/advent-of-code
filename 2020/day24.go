package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false
var dprint = tools.Absorb

var test = `
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew`[1:]

//go:embed day24.txt
var live string

type Point = tools.Point



// The world is hexes.  Hexes in a row are separated
// by 2 grid units.

//   (-1,-1)  (1,-1)
//  (-2,0)     (2,0)
//   (-1,+1)  (1,1)

var moves = map[string]Point{
    "nw": Point{-1,-1},
    "ne": Point{1,-1},
    "e":  Point{2,0},
    "se": Point{1,1},
    "sw": Point{-1,1},
    "w":  Point{-2,0},
}


func ones(grid map[Point]bool) map[Point]bool {
	out := make(map[Point]bool)
	for k,v := range grid {
		if v {
			out[k] = true
		}
	}
	return out
}


func printgrid(blacks map[Point]bool) {
	minx, maxx, miny, maxy := tools.Span(tools.Keys(blacks))
   // print( '     ' + ' '.join((' -'[d<0] for d in range(minx,maxx))))
   // print( '    ' + ''.join(('%2d'%abs(d) for d in range(minx,maxx))))
	for y := miny; y < maxy; y++ {
		ln := []byte(fmt.Sprintf("%3d", y)+strings.Repeat(" ",(maxx-minx+1)*2))
		for x := miny; x < maxy; x++ {
            if blacks[Point{x,y}] {
				ln[(x-minx)*2+5] = 'X'
			}
		}
        fmt.Println(string(ln))
	}
}

func part1(data []string) map[Point]bool {
    blacks := make(map[Point]bool)
    for _,ln := range data {
        posn := Point{0,0}
		for i := 0; i < len(ln); i++ {
			if ln[i] == 'n' || ln[i] == 's' {
				posn = posn.Add(moves[ln[i:i+2]])
				i ++
			} else {
				posn = posn.Add(moves[ln[i:i+1]])
			}
		}
		blacks[posn] = !blacks[posn]
	}
    return ones(blacks)
}


//Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
//Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

func neighbors(blacks map[Point]bool, cell Point) int {
	sum := 0
	for _,dpt := range moves {
		if blacks[cell.Add(dpt)] {
			sum++
		}
	}
	return sum
}

func cycle( blacks map[Point]bool ) map[Point]bool {
	minx, maxx, miny, maxy := tools.Span(tools.Keys(blacks))
	nxt := make(map[Point]bool)
	for x := minx-1; x <= maxx+1; x++ {
		for y := miny-1; y <= maxy+1; y++ {
			cell := Point{x,y}
            blks := neighbors( blacks, cell )
			if blacks[cell] && (blks == 1 || blks == 2) {
				nxt[cell] = true
			} else if !blacks[cell] && blks == 2 {
                nxt[cell] = true
			}
		}
	}
    return nxt
}


func part2(blacks map[Point]bool) map[Point]bool {
	for day := range 100 {
		blacks = cycle(blacks)
		dprint(day+1, len(blacks))
	}
	return blacks
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	if DEBUG {
		dprint = fmt.Println
	}
	data := strings.Split(strings.TrimSpace(input), "\n")

	blacks := part1(data)
	dprint(blacks)
	if DEBUG {
		printgrid(blacks)
	}
	fmt.Println("Part 1:", len(blacks) )

	fmt.Println("Part 2:", len(part2(blacks)))
}


