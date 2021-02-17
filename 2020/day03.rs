use std::env;

fn generate ( dx: usize, dy: usize, limx: usize, limy: usize ) -> Vec<(usize,usize)> {
    (0..).take_while(|i| *i*dy < limy)
        .map(|i| ((i*dx)%limx, i*dy))
        .collect()
}

fn import ( incoming : Vec::<&str> ) -> Vec<Vec<char>> {
    incoming
        .iter()
        .map(|x| x.chars().collect())
        .collect()
}

fn counttrees( grid : &Vec<Vec<char>>, dx: usize, dy: usize ) -> usize {
    generate( dx, dy, grid[0].len(), grid.len() )
        .iter()
        .filter(|(x,y)| grid[*y][*x] == '#')
        .count()
}

pub fn main() {
    let live = if env::args().any(|x| x == "test") 
    {
        import( vec![
            "..##.......",
            "#...#...#..",
            ".#....#..#.",
            "..#.#...#.#",
            ".#...##..#.",
            "..#.##.....",
            ".#.#.#....#",
            ".#........#",
            "#.##...#...",
            "#...##....#",
            ".#..#...#.#"
        ])
    } else {
        include_str!("day03.txt")
            .lines()
            .map(|x| x.chars().collect())
            .collect()
    };

    let counts : Vec<usize> = 
        [(1,1),(3,1),(5,1),(7,1),(1,2)]
        .iter()
        .map(|(x,y)| counttrees( &live, *x, *y ) )
        .collect();


    println!("Part 1: {}", counts[1] );
    println!("Part 2: {}", counts.iter().fold(1, |tot,i| tot * i ) );
}
