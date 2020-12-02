package main

import (
	"Fmt"
	"bufio"
	"os"
	"strconv"
)

func fuel1(mass int) int {
	return mass/3 - 2
}

func fuel2(mass int, sum int) int {
	f := fuel1(mass)
	if f <= 0 {
		return sum
	}
	return fuel2(f, sum+f)
}

func fuel(which int, mass int) int {
	if which == 1 {
		return fuel1(mass)
	} else {
		return fuel2(mass, 0)
	}
}

func main() {
	which, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Println("Pass part number, 1 or 2")
		return
	}

	tests := [...]int{12, 14, 1969, 100756}
	for _, test := range tests {
		fmt.Println(fuel(which, test))
	}

	file, _ := os.Open("day01.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)
	sum := 0
	for scanner.Scan() {
		in, _ := strconv.Atoi(scanner.Text())
		sum += fuel(which, in)
	}
	fmt.Println(sum)
}
