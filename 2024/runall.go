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

func main() {
	fmt.Println(ljust("Python", 30), ljust("C++", 30), "Go")
	fmt.Println(strings.Repeat("-", 90))

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
		for i := 0; i < len(gather[0]); i++ {
			if len(gather[0][i]) < 1 {
				break
			}
			for _, ln := range gather {
				fmt.Print(ljust(ln[i], 30))
			}
			fmt.Println()
		}
		for _, d := range times {
			fmt.Printf("%10.3f", d.Seconds())
			fmt.Print(strings.Repeat(" ", 20))
		}
		fmt.Println()
	}
}
