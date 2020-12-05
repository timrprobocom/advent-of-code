package main

import (
	"Fmt"
	"bufio"
	"os"
	"sort"
)

func main() {
	file, _ := os.Open("day05.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var seats []int;
	for scanner.Scan() {
		seat := 0
                ln := scanner.Text()
		for _, c := range ln {
			seat = seat * 2
			if c == 'B' || c == 'R' {
				seat += 1
			}
		}
                seats = append( seats, seat )
	}
	sort.Ints( seats )
	fmt.Println("Part 1: ",seats[len(seats)-1])

        last := 0
        for _, seat := range seats {
            if last > 0 && seat != last+1 {
                break
            }
            last = seat
        }
        fmt.Println( "Part 2: ", last+1 )
}
