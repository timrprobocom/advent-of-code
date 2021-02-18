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

struct NeighborCounter1 {
}

struct NeighborCounter2 {
    maxx: i32,
    maxy: i32,
}

trait NeighborCounter {
    fn count( &self, cell : Cell, seats: &Grid, occupied: &Grid ) -> i32;
}

impl NeighborCounter1 {
    fn new( ) -> Self {
        NeighborCounter1 { }
    }
}

impl NeighborCounter for NeighborCounter1 {
    fn count( &self, cell : Cell, _seats: &Grid, occupied: &Grid ) -> i32 {
        let deltas = iproduct!( -1..2, -1..2 ).filter(|x| *x != (0,0) );
        let (x,y) = cell;
        deltas
            .filter(|(dx,dy)| occupied.contains(&(x+dx,y+dy)))
            .count() as i32
    }
}

impl NeighborCounter2 {
    fn new( maxima : (i32,i32) ) -> Self {
        NeighborCounter2 { maxx: maxima.0, maxy: maxima.1 }
    }
}

impl NeighborCounter for NeighborCounter2 {
    fn count( &self, cell : Cell, seats: &Grid, occupied: &Grid ) -> i32 {
        let deltas = iproduct!( -1..2, -1..2 ).filter(|x| *x != (0,0) );

        let mut neighbors = 0;
        for (dx,dy) in deltas {
            let mut x = cell.0+dx;
            let mut y = cell.1+dy;
            while 0 <= x && x <= self.maxx && 0 <= y && y <= self.maxy {
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
}


fn passstep(counter: &dyn NeighborCounter, seats : &Grid, occupied : &Grid, criteria: i32) -> Grid {

    Grid::from_iter(
        seats
            .iter()
            .map(      |cell| (cell, counter.count( *cell, &seats, &occupied )) )
            .filter(   |&(cell,count)| (count == 0 || (occupied.contains(&cell) && count < criteria)) )
            .map(      |(cell,_)| *cell )
    )
}


fn main() {
    let debug : bool = env::args().any(|x| x=="debug");

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
    let counter1 = NeighborCounter1::new( );
    let counter2 = NeighborCounter2::new( (xlen, ylen) );

    let seats = translate( &data );
    let mut occupied = Grid::new();
    loop {
        let occ2 = passstep( &counter1, &seats, &occupied, 4 );
        if occupied == occ2 {
            break;
        };
        occupied = occ2.clone();
        if debug {
            println!( "{}", occ2.len() )
        }
    }

    println!( "Part 1: {}", occupied.len() );

    let mut occupied = Grid::new();
    loop {
        let occ2 = passstep( &counter2, &seats, &occupied, 5 );
        if occupied == occ2 {
            break;
        };
        occupied = occ2.clone();
        if debug {
            println!( "{}", occ2.len() )
        }
    }

    println!( "Part 2: {}", occupied.len() );
}


