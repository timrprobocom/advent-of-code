use itertools::iproduct;
use std::collections::HashSet;
use std::iter::FromIterator;
use std::env;


type Cell = (i32,i32,i32,i32);

type Grid = HashSet::<Cell>;

fn translate(data : &Vec<String>) -> Grid {
    let mut grid = Grid::new();

    for (y,ln) in data.iter().enumerate() {
        for (x,c) in ln.chars().enumerate() {
            if c == '#' {
                grid.insert( (x as i32,y as i32,0,0) );
            }
        }
    };

    grid
}

fn countneighbors( cell : Cell, grid : &Grid ) -> i32 {
    let adjacent = iproduct!( -1..2, -1..2, -1..2, -1..2 )
        .filter(|x| *x != (0,0,0,0) );

    let (x,y,z,w) = cell;
    adjacent
        .filter(|(dx,dy,dz,dw)| grid.contains(&(x+dx,y+dy,z+dz,w+dw)))
        .count() as i32
}

fn minmax(state : &Grid ) -> (i32,i32,i32,i32,i32,i32,i32,i32) {
    (
        *state.iter().map( |(x,_,_,_)| x ).min().unwrap(),
        *state.iter().map( |(_,y,_,_)| y ).min().unwrap(),
        *state.iter().map( |(_,_,z,_)| z ).min().unwrap(),
        *state.iter().map( |(_,_,_,w)| w ).min().unwrap(),
        *state.iter().map( |(x,_,_,_)| x ).max().unwrap(),
        *state.iter().map( |(_,y,_,_)| y ).max().unwrap(),
        *state.iter().map( |(_,_,z,_)| z ).max().unwrap(),
        *state.iter().map( |(_,_,_,w)| w ).max().unwrap()
    )
}

fn nextstate(state : &Grid, part: i32) -> Grid {
    let (minx,miny,minz,minw,maxx,maxy,maxz,maxw) = minmax(state);
    let wrange = if part==1 { 0..1 } else { minw-1..maxw+2 };

    HashSet::from_iter(
        iproduct!( minx-1..maxx+2, miny-1..maxy+2, minz-1..maxz+2, wrange )
            .map(      |cell| (cell, countneighbors( cell, &state )) )
            .filter(   |&(cell,count)| (count == 3 || (state.contains(&cell) && count == 2)) )
            .map(      |(cell,_)| cell )
    )
}

fn main() {
    let data : Vec<String> = if env::args().any(|x| x=="test")  {
        vec![
            ".#.".to_string(),
            "..#".to_string(),
            "###".to_string()
        ]
    } else {
        include_str!("../../day17.txt")
            .lines()
            .map(|x| x.to_string())
            .collect()
    };

    let mut state = translate( &data );
    for _ in 1..7 {
        state = nextstate( &state, 1 );
        println!( "{}", state.len() )
    }

    println!( "Part 1: {}", state.len() );

    let mut state = translate( &data );
    for _ in 1..7 {
        state = nextstate( &state, 2 );
        println!( "{}", state.len() )
    }

    println!( "Part 2: {}", state.len() )
}
