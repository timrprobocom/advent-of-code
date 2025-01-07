use std::env;

fn pass1 ( left: &Vec<i32>, right: &Vec<i32> ) -> i32 
{
    return left.iter().zip(right.iter())
        .map(|(a,b)| (a-b).abs())
        .sum();
}

fn pass2 ( left: &Vec<i32>, right: &Vec<i32> ) -> i32 
{
    return left.iter()
        .map(|a| a * (right.iter().filter(|&n| n==a).count() as i32))
        .sum();
}

pub fn main() 
{
    let test = "\
3   4
4   3
2   5
1   3
3   9
3   3";

    // Read.

    let data = if env::args().any(|x| x == "test") 
    {
        test
    }
    else 
    {
        include_str!("day01.txt")
    };

    // Parse.

    let mut left : Vec<i32> = Vec::new();
    let mut right : Vec<i32> = Vec::new();
    for line in data.lines()
    {
        let mut split = line
            .split_whitespace()
            .map(|i| i.parse::<i32>().unwrap());
            left.push( split.next().unwrap() );
            right.push( split.next().unwrap() );
    }
    left.sort();
    right.sort();

    // Process.

    println!( "Pass 1: {}", pass1( &left, &right));
    println!( "Pass 2: {}", pass2( &left, &right));
}
