use itertools::iproduct;
use std::collections::HashSet;
use std::iter::FromIterator;
use std::env;

static TEST : [&str; 10] = 
[
    "L.LL.LL.LL",
    "LLLLLLL.LL",
    "L.L.L..L..",
    "LLLL.LL.LL",
    "L.LL.LL.LL",
    "L.LLLLL.LL",
    "..L.L.....",
    "LLLLLLLLLL",
    "L.LLLLLL.L",
    "L.LLLLL.LL"
];

type Cell = (i32,i32);

type Grid = HashSet::<Cell>;

fn translate(data : &Vec<String>) -> Grid {
    let mut grid = Grid::new();

    for (y,ln) in data.iter().enumerate() {
        for (x,c) in ln.chars().enumerate() {
            if c == 'L' {
                grid.insert( (x as i32,y as i32) );
            }
        }
    };

    grid
}

fn countneighbors( cell : Cell, seats: &Grid, occupied: &Grid ) -> i32 {
    let deltas = iproduct!( -1..2, -1..2 ).filter(|x| *x != (0,0) );
    let (x,y) = cell;
    deltas
        .filter(|(dx,dy)| occupied.contains(&(x+dx,y+dy)))
        .count() as i32
}

fn countneighbors2( cell : Cell, maxima : (i32,i32), seats: &Grid, occupied: &Grid ) -> i32 {
    let (xlen,ylen) = maxima;
    let deltas = iproduct!( -1..2, -1..2 ).filter(|x| *x != (0,0) );

    let mut neighbors = 0;
    for (dx,dy) in deltas {
        let mut x = cell.0+dx;
        let mut y = cell.1+dy;
        while 0 <= x && x <= xlen && 0 <= y && y <= ylen {
            if seats.contains(&(x,y)) {
                if occupied.contains(&(x,y)) {
                    neighbors += 1
                }
                break
            }
            x = x + dx;
            y = y + dy;
        }
    }

    neighbors
}


fn pass1step(_maxima : (i32,i32), seats : &Grid, occupied : &Grid, criteria: i32) -> Grid {

/*
    let mut result = Grid::new();
    for cell in seats {
        let n = countneighbors( *cell, &seats, &occupied );
        if n == 0 || (occupied.contains(&cell) && n < criteria)  {
            result.insert( *cell );
        }
    };
    result
*/
    Grid::from_iter(
        seats
            .iter()
            .map(      |cell| (cell, countneighbors( *cell, &seats, &occupied )) )
            .filter(   |&(cell,count)| (count == 0 || (occupied.contains(&cell) && count < criteria)) )
            .map(      |(cell,_)| *cell )
    )
}

fn pass2step(maxima : (i32,i32), seats : &Grid, occupied : &Grid, criteria: i32) -> Grid {

    Grid::from_iter(
        seats
            .iter()
            .map(      |cell| (cell, countneighbors2( *cell, maxima, &seats, &occupied )) )
            .filter(   |&(cell,count)| (count == 0 || (occupied.contains(&cell) && count < criteria)) )
            .map(      |(cell,_)| *cell )
    )
}

fn main() {
    let data : Vec<String> = if env::args().any(|x| x=="test")  {
        TEST
            .iter()
            .map(|x| x.to_string())
            .collect()
    } else {
        include_str!("../../day11.txt")
            .lines()
            .map(|x| x.to_string())
            .collect()
    };

    let xlen = data[0].len() as i32;
    let ylen = data.len() as i32;

    let seats = translate( &data );
    let mut occupied = Grid::new();
    loop {
        let occ2 = pass1step( (xlen,ylen), &seats, &occupied, 4 );
        if occupied == occ2 {
            break;
        };
        occupied = occ2.clone();
//        println!( "{}", occ2.len() )
    }

    println!( "Part 1: {}", occupied.len() );

    let mut occupied = Grid::new();
    loop {
        let occ2 = pass2step( (xlen,ylen), &seats, &occupied, 5 );
        if occupied == occ2 {
            break;
        };
        occupied = occ2.clone();
//        println!( "{}", occ2.len() )
    }

    println!( "Part 2: {}", occupied.len() );
}


