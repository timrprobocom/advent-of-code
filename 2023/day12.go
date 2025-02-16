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
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1`[1:]

//go:embed day12.txt
var live string

// Does chk match the first pat of pat?

func match(pat string, chk string) bool {
	for i := range min(len(chk), len(pat)) {
		if pat[i] != chk[i] && pat[i] != '?' {
			return false
		}
	}
	return true
}

// Each call of this does one chunk of #s.  We generage all possible strings that
// end with "###." for this chunk.  If that prefix matches the current spot in the
// pattern, we recursively try the next.  Its only the memoizing that allows
// this to run in finite time.

type Cache struct {
	pat  string
	size int
	nums uint64
}

func hash(nums []int) uint64 {
	var h uint64 = 0
	for _, i := range nums {
		h = h*13 + uint64(i)
	}
	return h
}

var cache map[Cache]int

func gen(pat string, size int, nums []int) int {
	if len(nums) == 0 {
		if strings.Contains(pat, "#") {
			return 0
		} else {
			return 1
		}
	}

	entry := Cache{pat, size, hash(nums)}
	if cache[entry] > 0 {
		return cache[entry] - 1
	}

	now := nums[0]
	rest := nums[1:]
	after := tools.Sum(rest) + len(rest)

	count := 0

	for before := range size - after - now + 1 {
		s := strings.Repeat(".", before) + strings.Repeat("#", now) + "."
		if match(pat, s) {
			n := min(len(pat), len(s))
			count += gen(pat[n:], size-now-before-1, rest)
		}
	}
	cache[entry] = count + 1
	return count
}

func count_matches(pat string, nums []int) int {
	return gen(pat, len(pat), nums)
}

type Context struct {
	pat  string
	nums []int
}

func part1(data []Context) int {
	sum := 0
	for _, ctx := range data {
		sum += count_matches(ctx.pat, ctx.nums)
	}
	return sum
}

func part2(data []Context) int {
	sum := 0
	for _, ctx := range data {
		pat := ctx.pat + "?" + ctx.pat + "?" + ctx.pat + "?" + ctx.pat + "?" + ctx.pat
		nums := []int{}
		for range 5 {
			nums = append(nums, ctx.nums...)
		}
		sum += count_matches(pat, nums)
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	// Parse the input.

	data := []Context{}
	for _, row := range strings.Split(input, "\n") {
		maps, snums, _ := strings.Cut(row, " ")
		nums := tools.SplitIntBy(snums, ",")
		data = append(data, Context{maps, nums})
	}
	cache = make(map[Cache]int)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
