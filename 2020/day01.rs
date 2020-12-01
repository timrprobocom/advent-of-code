use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn pass1 ( values: &Vec<i32> ) -> i32 {
    for t1 in values {
        for t2 in values {
            if t1+t2 == 2020 {
                return t1*t2;
            }
        }
    }
    return 0;
}

fn pass2 ( values: &Vec<i32> ) -> i32 {
    for t1 in values {
        for t2 in values {
            for t3 in values {
                if t1+t2+t3 == 2020 {
                    return t1*t2*t3;
                }
            }
        }
    }
    return 0;
}


fn main() {

    let test = vec![ 1721, 979, 366, 299, 675, 1456 ];
    println!( "{}", pass1( &test ));
    println!( "{}", pass2( &test ));

    let mut live: Vec<i32> = Vec::new();
    if let Ok(lines) = read_lines("day01.txt") {
        for line in lines {
            if let Ok(ln) = line {
                if let Ok(amt) = ln.parse::<i32>() {
                    live.push( amt );
                }
            }
        }
    }
    println!( "Pass 1: {}", pass1( &live ));
    println!( "Pass 2: {}", pass2( &live ));
}

// What the hell is this doing?

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
