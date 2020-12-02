#! /bin/tclsh

set test {
"1-3 a: abcde"
"1-3 b: cdefg"
"2-9 c: ccccccccc"
}

proc pass1 line {
    set parts [ split $line ]
    set p1 [ split [ lindex $parts 0 ] '-' ]
    set a [ lindex $p1 0 ]
    set b [ lindex $p1 1 ]
    set target [ string index [ lindex $parts 1 ] 0 ]
    set haystack [ lindex $parts 2 ]
#    puts "$a $b $target $haystack"
    set bigger [ string map "$target XX" $haystack ]
    set count [ expr [ string length $bigger ] - [ string length $haystack ] ]
    expr $count >= $a && $count <= $b
}

proc pass2 line {
    set parts [ split $line ]
    set p1 [ split [ lindex $parts 0 ] '-' ]
    set a [ lindex $p1 0 ]
    set b [ lindex $p1 1 ]
    set target [ string index [ lindex $parts 1 ] 0 ]
    set haystack [ lindex $parts 2 ]
    expr {([string index $haystack $a] == $target) != ([string index $haystack $b] == $target)}
}

proc evaluate1 lines {
    set sum 0
    foreach line $lines {
        if { [ string length $line ] } {
            set sum [ expr $sum + [ pass1 $line ]]
        }
    }
    expr $sum
}

proc evaluate2 lines {
    set sum 0
    foreach line $lines {
        if { [ string length $line ] } {
            set sum [ expr $sum + [ pass2 $line ]]
        }
    }
    expr $sum
}

set live [split [read [open "day02.txt" r ]] "\n" ]

puts "2: [evaluate1 $test]"
puts "Part 1: [evaluate1 $live]"
puts "1: [evaluate2 $test]"
puts "Part 2: [evaluate2 $live]"

