use std::env;


fn common( bits : usize, data : &Vec<u32> ) -> (u32, u32)
{
    // We need to enumerate vertically here.

    let num: usize = data.len();
    let mut counts = vec![0; bits];

    for row in data {
        for i in 0..32 {
            if row & (1 << i) > 0 {
                counts[i] += 1;
            }
        }
    }

    let mut res : u32 = 0;
    for i in (0..bits).rev()
    {
        res = res * 2 + if counts[i] * 2 >= num { 1 } else { 0 };
    }

    let allone: u32 = (1 << bits) - 1;
    (res, allone-res)
}

fn part1( bits: usize, data: &Vec<u32> ) -> u32
{
    let (most, least) = common(bits, data);
    most * least
}

fn part2( bits: usize, data: &Vec<u32> ) -> u32
{
    let mut hdata = data.to_owned();
    let mut ldata = data.to_owned();

    for bitno in 0..bits {
        let bit = 1 << (bits-bitno-1);

        if hdata.len() > 1 {
            let (most,_least) = common(bits, &hdata);
            let crit = bit & most;
            hdata = hdata
                .into_iter()
                .filter(|row| row & bit == crit)
                .collect();
        }

        if ldata.len() > 1 {
            let (_most,least) = common(bits, &ldata);
            let crit = bit & least;
            ldata = ldata
                .into_iter()
                .filter(|row| row & bit == crit)
                .collect();
        }

        if hdata.len() == 1 && ldata.len() == 1 {
            break;
        }
    }

    println!("{} {}", hdata[0], ldata[0]);

    hdata[0] * ldata[0]
}



static TEST : [&str; 12] = 
[
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
];

pub fn main() {
    let live : Vec<u32> = if env::args().any(|x| x == "test")
    {
        TEST
            .iter()
            .map(|x| u32::from_str_radix(x,2).unwrap() )
            .collect()
    } else {
        include_str!("day03.txt")
            .lines()
            .map(|x| u32::from_str_radix(x,2).unwrap() )
            .collect()
    };

    let binsum = live.iter().fold(0, |accum,item| accum | item ) + 1;
    let mut bits : usize = 0;
    for i in 0..32 {
        if binsum == 1<<i {
            bits = i;
            break;
        }
    }

    println!( "Pass 1: {}", part1( bits, &live ));
    println!( "Pass 2: {}", part2( bits, &live ))
}
