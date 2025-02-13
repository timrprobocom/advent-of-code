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
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4`[1:]

//go:embed day05.txt
var live string

type OneMap struct {
	dest int64
	src  int64
	size int64
}

func (om OneMap) endof() int64 {
	return om.src+om.size
}

// Convert the input into a list of seed numbers, and a
// list of maps.  Each map is a list of tuples, (dest,src,len).

func convert(data []string) (seeds []int64, maps [][]OneMap) {
	var lastmap []OneMap
	for _, row := range data {
		if strings.HasPrefix(row, "seeds") {
			seeds = tools.SplitInt64(row)
		} else if len(row) < 2 {
			if len(lastmap) > 0 {
				slices.SortFunc(lastmap, func(a, b OneMap) int { return int(a.src - b.src) })
				maps = append(maps, lastmap)
				lastmap = []OneMap{}
			}
		} else if tools.Isdigit(row[0]) {
			vals := tools.SplitInt64(row)
			lastmap = append(lastmap, OneMap{vals[0], vals[1], vals[2]})
		}
	}
	slices.SortFunc(lastmap, func(a, b OneMap) int { return int(a.src - b.src) })
	maps = append(maps, lastmap)
	return seeds, maps
}

// Map a single value through a single map.

func mapping(mapx []OneMap, value int64) int64 {
	for _, om := range mapx {
		if tools.Between(om.src, value, om.endof()+1) {
			return value - om.src + om.dest
		}
	}
	return value
}

// Map a single value through all of the maps.

func domapping(maps [][]OneMap, value int64) int64 {
	for _, m := range maps {
		value = mapping(m, value)
	}
	return value
}

func part1(seeds []int64, maps [][]OneMap) int64 {
	var m int64 = 1e11
	for _, s := range seeds {
		m = min(m, domapping(maps, s))
	}
	return m
}

// We need to intersect the ranges.
// There are 3 cases to consider:
//   * The range starts before any map
//   * The range intersects one or more maps
//   * The range extends beyond the last map
//
//  So given 79,14  against 50,98,2 and 52,50,48
//    We get 79,14 had a delta of +2
//  Given 40,70  against 50,98,2 and 52,50,48
//    We get 40,10 with delta 0
//           50,48 with a delta of +2
//           98,2 with a delta of -48
//           100,10 with a delta of 0

type Range struct {
	lo   int64
	size int64
}

// Map a single range through a single map.

func maprange(mapx []OneMap, rng Range) []Range {
	rnglo := rng.lo
	rnghi := rnglo + rng.size
	var res []Range
	m := mapx[0]
	if rnglo < m.src {
		take := min(rnghi, m.src) - rnglo
		res = append(res, Range{rnglo, take})
		rnglo += take
	}
	if rnglo == rnghi {
		return res
	}
	// We now know that rnglo is at or beyond the first map.

	for _, m := range mapx {
		if rnglo <= m.endof() {
			take := min(rnghi, m.endof()) - rnglo
			res = append(res, Range{rnglo - m.src + m.dest, take})
			rnglo += take
		}
		if rnglo == rnghi {
			return res
		}
	}
	if rnglo < rnghi {
		res = append(res, Range{rnglo, rnghi - rnglo})
	}
	return res
}

// Map a set of ranges through a single map.

func domapranges(mapx []OneMap, rngs []Range) []Range {
	var res []Range
	for _, r := range rngs {
		res = append(res, maprange(mapx, r)...)
	}
	return res
}

// Map a set of ranges through all of the maps.

func doallmapranges(maps [][]OneMap, rngs []Range) []Range {
	for _, m := range maps {
		rngs = domapranges(m, rngs)
	}
	return rngs
}

func part2(part int, seeds []int64, maps [][]OneMap) int64 {
	var ranges []Range
	if part == 1 {
		for _, s := range seeds {
			ranges = append(ranges, Range{s, 1})
		}
	} else {
		for i := 0; i < len(seeds); i += 2 {
			ranges = append(ranges, Range{seeds[i], seeds[i+1]})
		}
	}
	ranges = doallmapranges(maps, ranges)
	minval := ranges[0].lo
	for _, a := range ranges {
		minval = min(minval, a.lo)
	}
	return minval
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	seeds, maps := convert(data)

	if DEBUG {
		fmt.Println(seeds, maps)
		fmt.Println(domapranges(maps[0], []Range{{79, 14}}))
		fmt.Println(domapranges(maps[0], []Range{{40, 70}}))
	}

	//fmt.Println("Part 1:", part1(seeds, maps))
	fmt.Println("Part 1:", part2(1, seeds, maps))
	fmt.Println("Part 2:", part2(2, seeds, maps))
}
