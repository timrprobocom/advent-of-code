package main

import (
	"fmt"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

const test = "2333133121414131402"

//go:embed day09.txt
var live string

var WIDTH = -1
var HEIGHT = -1


func part1(data []int) int64 {
    idn := 0
    var disk []int

	for i, size := range data {
		if i % 2 > 0 {
			disk = append( disk, tools.Repeat(-1, size)...)
		} else {
			disk = append( disk, tools.Repeat(idn, size)...)
			idn++
		}
	}

    // Now compact it.
    i := 0
    j := len(disk)-1

	for i < j {
		for disk[i] >= 0 {
			i++
		}
		for disk[j] < 0 {
			j--
		}
		if i < j {
			disk[i] = disk[j]
			disk[j] = -1
			i++
			j--
		}
	}

    if DEBUG {
        fmt.Println(disk)
	}

    // Evaluate.

    var sum int64 = 0
    for n,i := range disk {
        if i >= 0 {
            sum += int64(n)*int64(i)
		}
	}
	return sum
}

type Entry struct {
	start int
	size int
	idn int
}

// Combine free blocks and remove empty ones.

func coalesce( space []Entry, start int, size int ) []Entry {
    var newspace []Entry
	done := false
	for _, entry := range space {
		if done {
			newspace = append( newspace, entry )
			continue
		}
        if entry.size==0 {
            continue
		} else if start > entry.start+entry.size {
            newspace = append( newspace, Entry{entry.start, entry.size,0} )
        } else if start+size == entry.start {
            newspace = append( newspace, Entry{start, size+entry.size, 0} )
            done = true
		} else if entry.start+entry.size == start {
            newspace = append( newspace, Entry{entry.start, size+entry.size, 0} )
            done = true
		} else if entry.start > start+size {
            newspace = append( newspace, Entry{start, size,0} )
            newspace = append( newspace, entry )
            done = true
		}
	}
    return newspace
}

// Find the first hold large enough to hold this file.

func find_hole_below( space []Entry, start int, size int ) int {
    for i,s := range space {
        if s.start > start {
            return -1
		}
        if s.size >= size {
            return i
		}
	}
    return -1
}

func part2(data []int) int64 {
    locate := 0
	var files []Entry
	var space []Entry

	for i, size := range data {
        if i % 2 == 0 {
            files = append( files, Entry{locate, size, len(files)} )
		} else if size > 0 {
            space = append( space, Entry{locate, size, 0} )
		}
        locate += size
	}

    if DEBUG {
        print(files)
        print(space)
	}

    // Now try to move all the files starting from the end.

    reversed := slices.Clone(files)
	slices.Reverse(reversed)
    for _, entry := range reversed {
        n := find_hole_below( space, entry.start, entry.size )
        if n >= 0 {
            // Move this file.  Reduce empty space.
            files[entry.idn].start = space[n].start
            space[n].start += entry.size
            space[n].size  -= entry.size
            space = coalesce(space, entry.start, entry.size)
		}
	}
    
    if DEBUG {
        slices.SortFunc(files, func(a Entry, b Entry) int { return a.start-b.start })
        fmt.Println(files)
        fmt.Println(space)
	}

    // Evaluate.

	var sum int64 = 0
    for _, entry := range files {
		for s := 0; s < entry.size; s++ {
			sum += int64(entry.start + s) * int64(entry.idn)
		}
	}
    return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
    var data []int
	for _, c := range input {
		data = append(data, int(byte(c)-'0'))
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

