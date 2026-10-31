package main

import (
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

func ljust(s string, w int) string {
	if len(s) >= w {
		return s
	}
	return s + strings.Repeat(" ", w-len(s))
}

func fetch(cmd string, args ...string) (string, time.Duration) {
	sub := exec.Command(cmd, args...)
	before := time.Now()
	output, err := sub.Output()
	delta := time.Since(before)
	if err != nil {
		fmt.Println("Error", err, "calling", cmd)
		return "Error", time.Duration(0)
	}
	return string(output), delta
}

// Why does Go have 0.1s 0.2s overhead on MacOS when Python does not?
// And why does it not when run by Python 3.15?  Even running the
// "time" command inside exec.Command has it!!!

func fetch1(cmd string, args ...string) (string, time.Duration) {
	argx := "time " + cmd + " " + strings.Join( args, " ")
	sub := exec.Command("bash", "-c", argx)
	fmt.Println(argx)
	var outf strings.Builder
	var errf strings.Builder
	sub.Stdout = &outf
	sub.Stderr = &errf
	before := time.Now()
	err := sub.Run()
	delta := time.Since(before)
	if err != nil {
		fmt.Println("Error", err, "calling", cmd)
		return "Error", time.Duration(0)
	}
	fmt.Println("stderr", errf.String(), "***")
	return outf.String(), delta
}


func prep(file string, ext string) {
	if ext == ".cpp" {
		os.Remove(file)
		sub := exec.Command("g++", "--std=c++17", "-O3", "-o", file, file+ext, "-llapack")
		sub.Stdout = os.Stdout
		sub.Stderr = os.Stderr
		sub.Run()
	} else if ext == ".go" {
		os.Remove(file)
		sub := exec.Command("go", "build", file+ext)
		sub.Stdout = os.Stdout
		sub.Stderr = os.Stderr
		sub.Run()
	}
}

func run(file string, ext string) (string, time.Duration) {
	if ext == ".py" {
		return fetch("python", file+ext)
	} else {
		return fetch("./" + file)
	}
	return "", time.Duration(0)
}

const FIELD int = 40

func main() {
	FIRST := 1
	LAST := 25
    if len(os.Args) == 2 {
		LAST,_ = strconv.Atoi(os.Args[1])
	} else if len(os.Args) == 3 {
		FIRST,_ = strconv.Atoi(os.Args[1])
		LAST,_ = strconv.Atoi(os.Args[2])
	}

	stats_csv, _ := os.Create("times.csv")
	defer stats_csv.Close()
	fmt.Println(ljust("Python", FIELD) + ljust("C++", FIELD) + "Go")
	fmt.Println(strings.Repeat("-", 3*FIELD))

	sums := []float64{0, 0, 0}
	for day := FIRST; day <= LAST; day++ {
		fn := fmt.Sprintf("day%02d", day)

		var gather [][]string
		var times []time.Duration
		for _, lang := range []string{".py", ".cpp", ".go"} {
			if _, err := os.Stat(fn + lang); err == nil {
				prep(fn, lang)
				s, elapsed := run(fn, lang)
				times = append(times, elapsed)
				gather = append(gather, strings.Split(s, "\n"))
			} else {
				times = append(times, time.Duration(0) )
				gather = append(gather, []string{""})
			}
		}

		if len(gather) == 0 {
			continue
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
				if i >= len(ln) {
					fmt.Print(strings.Repeat(" ", FIELD))
				} else if len(ln[i]) > FIELD {
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
		if len(gather) > 1 && len(gather[1][0]) > 0 && strings.Join(gather[0], "") != strings.Join(gather[1], "") {
			fmt.Println("#### Python and C++ results do not match ####")
		}
		if len(gather) > 2 && len(gather[2][0]) > 0 && strings.Join(gather[0], "") != strings.Join(gather[2], "") {
			fmt.Println("#### Python and Go results do not match ####")
		}
		for i, d := range times {
			sums[i] += d.Seconds()
			if d.Seconds() > 0 {
				fmt.Printf("%10.6f", d.Seconds())
				fmt.Print(strings.Repeat(" ", FIELD-10))
			} else {
				fmt.Print(strings.Repeat(" ",FIELD))
			}
			if i > 0 {
				stats_csv.Write([]byte(","))
			}
			fmt.Fprint(stats_csv, d.Seconds())
		}
		fmt.Println()
		stats_csv.Write([]byte("\n"))
	}
	fmt.Println("\nTotals:")
	for _, d := range sums {
		fmt.Printf("%10.6f s", d)
		fmt.Print(strings.Repeat(" ", FIELD-12))
	}
	fmt.Println()
}
