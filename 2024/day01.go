package main

import (
	"fmt"
	"bufio"
	"os"
	"sort"
        "strconv"
        "strings"
)

func absInt(x int) int {
   return absDiffInt(x, 0)
}

func absDiffInt(x, y int) int {
   if x < y {
      return y - x
   }
   return x - y
}

func Count( haystack []int, needle int ) int {
    count := 0
    for _, i := range haystack {
        if i==needle {
            count += 1
        }
    }
    return count
}

func part1( one []int, two []int ) int {
    sumx := 0
    for i, p1 := range one {
        sumx += absDiffInt(p1, two[i]);
    }
    return sumx
}

func part2( one []int, two []int ) int {
    sumx := 0
    for _, p1 := range one {
        sumx += p1 * Count(two, p1);
    }
    return sumx
}


func main() {
    file, _ := os.Open("day01.txt")
    defer file.Close()

    scanner := bufio.NewScanner(file)

    var one []int;
    var two []int;

    for scanner.Scan() {
        ln := scanner.Text()
        words := strings.Fields(ln)
        i, _ := strconv.Atoi(words[0])
        one = append( one, i )
        i, _  = strconv.Atoi(words[1])
        two = append( two, i )
    }
    sort.Ints( one )
    sort.Ints( two )
    fmt.Println("Part 1:", part1(one, two))
    fmt.Println("Part 2:", part2(one, two))
}
