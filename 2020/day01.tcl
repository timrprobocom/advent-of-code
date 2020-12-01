#! /usr/bin/tclsh

proc pass1 data {
    foreach t1 $data {
        foreach t2 $data {
            if { [expr { $t1+$t2 } ] == 2020 } {
                return [expr { $t1 * $t2 } ]
            }
        }
    }
    return 0
}

proc pass2 data {
    foreach t1 $data {
        foreach t2 $data {
            foreach t3 $data {
                if { [expr { $t1+$t2+$t3 } ] == 2020 } {
                    return [expr { $t1 * $t2 * $t3 } ]
                }
        }
        }
    }
    return 0
}

set test { 1721 979 366 299 675 1456 }

puts [ pass1 $test ]
puts [ pass2 $test ]

set live { }
set fp [open "day01.txt" r]
while { -1 != [gets $fp line] } {
    append live " " $line
}

puts "Pass 1: [ pass1 $live ] "
puts "Pass 2: [ pass2 $live ] "





