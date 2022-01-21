
fn pass1 ( values: &Vec<i32>, delta: usize ) -> i32 {
    return (0..values.len()-delta)
        .map(|i| values[i+delta]-values[i])
        .map(|t| if t > 0 { 1 } else { 0 })
        .sum();
}

pub fn main() {

    let test = vec![ 199, 200, 208, 210, 200, 207, 240, 269, 260, 263 ];
    println!( "{}", pass1( &test, 1 ));
    println!( "{}", pass1( &test, 3 ));

    let live = include_str!("day01.txt")
        .lines()
        .map( |i| i.parse::<i32>().unwrap() )
        .collect();

    println!( "Pass 1: {}", pass1( &live, 1 ));
    println!( "Pass 2: {}", pass1( &live, 3 ));
}
