
fn pass1 ( values: &Vec<i32> ) -> i32 {
    for t1 in values {
        for t2 in values {
            if t1+t2 == 2020 {
                return t1*t2;
            }
        }
    }
    0
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
    0
}

pub fn main() {

    let test = vec![ 1721, 979, 366, 299, 675, 1456 ];
    println!( "{}", pass1( &test ));
    println!( "{}", pass2( &test ));

    let live = include_str!("day01.txt")
        .lines()
        .map( |i| i.parse::<i32>().unwrap() )
        .collect();

    println!( "Pass 1: {}", pass1( &live ));
    println!( "Pass 2: {}", pass2( &live ));
}

