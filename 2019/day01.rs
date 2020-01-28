use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn fuel1 ( mass: i32 ) -> i32 {
    return mass / 3 - 2;
}

fn fuel2 ( mass: i32, sum: i32 ) -> i32 {
    let f = fuel1(mass);
    if f <= 0  {
        return sum;
    }
    return fuel2(f,sum+f);
}

fn main() {

    for test in [12,14,1969,100756].iter() {
        println!( "{}", fuel2(*test,0) );
    }

    let mut sum = 0;
    if let Ok(lines) = read_lines("day01.txt") {
        for line in lines {
            if let Ok(ln) = line {
                if let Ok(amt) = ln.parse::<i32>() {
                    sum += fuel2(amt, 0);
                }
            }
        }
    }
    println!( "{}", sum )

}

// What the hell is this doing?

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
