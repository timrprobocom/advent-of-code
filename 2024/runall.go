package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
	"time"
)

func ljust(s string, w int) string {
	if len(s) >= w {
		return s
	}
	return s + strings.Repeat(" ", w-len(s))
}

func fetch(cmd string, args ...string) string {
	sub := exec.Command(cmd, args...)
	output, err := sub.Output()
	if err != nil {
		fmt.Println("Error", err, "calling", cmd)
		return "Error"
	}
	return string(output)
}

func prep(file string, ext string) {
	if ext == ".cpp" {
		sub := exec.Command("g++", "--std=c++17", "-O3", "-o", file, file+ext, "-llapack")
		sub.Run()
	} else if ext == ".go" {
		sub := exec.Command("go", "build", file+ext)
		sub.Run()
	}
}

func run(file string, ext string) string {
	s := ""
	if ext == ".py" {
		s = fetch("python", file+ext)
	} else {
		s = fetch("./" + file)
	}
	return s
}

const FIELD int = 40

func main() {
	fmt.Println(ljust("Python", FIELD), ljust("C++", FIELD), "Go")
	fmt.Println(strings.Repeat("-", 3*FIELD))

	sums := []float64{0,0,0}
	for day := 1; day <= 25; day++ {
		fn := fmt.Sprintf("day%02d", day)
		var gather [][]string
		var times []time.Duration
		for _, lang := range []string{".py", ".cpp", ".go"} {
			if _, err := os.Stat(fn + lang); err == nil {
				prep(fn, lang)
				before := time.Now()
				s := run(fn, lang)
				times = append(times, time.Since(before))
				gather = append(gather, strings.Split(s, "\n"))
			}
		}

		fmt.Println(fn)
		pad := ""
		for i := 0; i < len(gather[0]); i++ {
			pad = ""
			if len(gather[0][i]) < 1 {
				break
			}
			for j, ln := range gather {
				fmt.Print(pad)
				if len(ln[i]) > FIELD {
					fmt.Println(ln[i])
					pad = strings.Repeat(" ", (j+1)*FIELD)
				} else {
					fmt.Print(ljust(ln[i], FIELD))
					pad = ""
				}
			}
			if len(pad) == 0 {
				fmt.Println()
			}
		}
		for i, d := range times {
			sums[i] += d.Seconds()
			fmt.Printf("%10.3f", d.Seconds())
			fmt.Print(strings.Repeat(" ", FIELD-10))
		}
		fmt.Println()
	}
    fmt.Println("\nTotals:")
	for _, d := range sums {
		fmt.Printf("%10.3f s", d)
		fmt.Print(strings.Repeat(" ", FIELD-8))
	}
	fmt.Println()
}
