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
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0`[1:]

var test2 = `
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1`[1:]

//go:embed day14.txt
var live string

func xlatemask1(mask string) (int, int) {
	mask0 := tools.StrToBin(strings.ReplaceAll(strings.ReplaceAll(mask, "1", "0"), "X", "1"))
	value := tools.StrToBin(strings.ReplaceAll(mask, "X", "0"))
	return mask0, value
}

func part1(data []string) int {
	memory := make(map[int]int)
	mask0 := 0
	value := 0
	for _,ln := range data {
		left, right, _ := strings.Cut(ln," = ")
		if left == "mask" {
			mask0, value = xlatemask1(right)
		} else {
			i := strings.IndexByte(ln, '[')
			j := strings.IndexByte(ln, ']')
			addr := tools.StrToInt(left[i+1 : j])
			val := tools.StrToInt(right)
			if DEBUG {
				fmt.Println(addr, val, (val&mask0)|value)
			}
			memory[addr] = (val & mask0) | value
		}
	}

	if DEBUG {
		fmt.Println(memory)
	}
	return tools.Sum(tools.Values(memory))
}

func xlatemask2( mask, addr string ) string {
	result := make([]byte, len(mask))
	for i := range len(mask) {
		if mask[i] == '0' {
			result[i] = addr[i]
		} else {
			result[i] = mask[i]
		}
	}
    return string(result)
}

func fmtbin( num int, dig int ) string {
	pat := make([]byte, dig)
	for i := range dig {
		if num & (1<<i) > 0 {
			pat[dig-i-1] = '1'
		} else {
			pat[dig-i-1] = '0'
		}
	}
	return string(pat)
}

func nextaddr(yield chan int, mask string) {
    // Find all the X.  Produce all 0,1 combos for the Xs.
	allxs := []int{}
	for i := range len(mask) {
		if mask[i] == 'X' {
			allxs = append(allxs, i)
		}
	}

	// This is counting all the binary numbers from 
	// 0 to 2^len(allxs)-1.

	for patnum := range 1 << len(allxs) {
		pat := fmtbin(patnum,len(allxs))
        e1 := []byte(mask)
		for i := range len(allxs) {
		    e1[allxs[i]] = pat[i]
		}
		yield <- tools.StrToBin(string(e1))
	}

	close(yield)
}

func invert(addr int) int {
    return addr ^ 0xfffffffff
}

func part2(data []string) int {

	// Construct the list of floating memory writes.

    type State struct {
		mask string
		xlate1 int
		xlate2 int
		value  int
	}

	memory := []State{}
	mask := ""
	for _,ln := range data {
		left, right, _ := strings.Cut(ln," = ")
		if left == "mask" {
			mask = right
		} else {
			i := strings.IndexByte(ln, '[')
			j := strings.IndexByte(ln, ']')
			addr := fmtbin(tools.StrToInt(left[i+1:j]), len(mask))
			val := tools.StrToInt(right)
			xm := xlatemask2(mask,addr)
            m,v := xlatemask1(xm)
			memory = append(memory, State{xm, invert(m), v, val} )
		}
	}
    if DEBUG {
		for _,m := range memory {
			fmt.Printf(" ('%s', %d, %d, %d),\n", m.mask, m.xlate1, m.xlate2, m.value )
		}
	}

	// For each write, for each variant of the address, if the address is not
	// matched by a future write, add it to the sum.

    sum := 0
	for i,pair := range memory {
		channel := make(chan int)
		go nextaddr(channel, pair.mask)
		for addr := range channel {
			winner := true
			for _,mem := range memory[i+1:] {
				if addr & mem.xlate1 == mem.xlate2 {
					winner = false
					break
				}
			}
			if winner {
				sum += pair.value
			}
		}
	}

    return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(strings.TrimSpace(input), "\n")

	fmt.Println("Part 1:", part1(data))
	if !TEST {
		fmt.Println("Part 2:", part2(data))
	}
}

