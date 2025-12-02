package main

import (
	"fmt"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124`[1:]

//go:embed day02.txt
var live string

func part1(data string) int {
	count := 0
	for _, row := range strings.Split(data, ",") {
		rg := strings.Split(row, "-")
		l := rg[0]
		r := rg[1]
		ln := tools.StrToInt(l)
		rn := tools.StrToInt(r)

		// If they are not the same length, adjust the odd one.
		// If left is odd, replace it by 1000.
		// If right is odd, replace it by 9999.
		if len(l)%2 > 0 {
			if len(r)%2 > 0 {
				continue
			} else {
				l = "1" + strings.Repeat("0", len(l))
			}
		} else if len(r)%2 > 0 {
			r = strings.Repeat("9", len(l))
		}

		// We can now assert that both numbers have an even number of digits.

		lhalf := l[0 : len(l)/2]
		lhalfn := tools.StrToInt(lhalf)
		rhalfn := tools.StrToInt(r[0:len(l)/2]) + 1

		for lhalfn < rhalfn {
			llln := tools.StrToInt(strconv.Itoa(lhalfn) + strconv.Itoa(lhalfn))
			if ln <= llln && llln <= rn {
				count += llln
			}
			lhalfn++
		}
		if DEBUG {
			fmt.Println(l, r, count)
		}
	}

	return count
}

// This is a shameful brute force approach.

func check(num int) bool {
	ns := strconv.Itoa(num)
	n := len(ns)
	for i := 1; i <= n/2; i++ {
		if n%i > 0 {
			continue
		}
		ok := true
		for j := i; j < n; j += i {
			if ns[j:j+i] != ns[:i] {
				ok = false
				break
			}
		}
		if ok {
			return true
		}
	}
	return false
}

func part2(data string) int {
	count := 0
	for _, row := range strings.Split(data, ",") {
		rg := strings.Split(row, "-")
		l := rg[0]
		r := rg[1]
		ln := tools.StrToInt(l)
		rn := tools.StrToInt(r)

		for n := ln; n <= rn; n++ {
			if check(n) {
				count += n
			}
		}
		if DEBUG {
			fmt.Println(l, r, count)
		}
	}
	return count
}

func main() {
	var data string
	TEST, DEBUG, data = tools.Setup(test, live)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
