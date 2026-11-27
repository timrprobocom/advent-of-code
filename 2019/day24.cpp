#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <cstdint>
#include <map>
#include <algorithm>
#include <numeric>

const char * input = 
    "...#."
    "#.##."
    "#..##"
    "#.###"
    "##...";

const char * test = 
    "....#"
    "#..#."
    "#..##"
    "..#.."
    "#....";

bool DEBUG = false;
bool TEST = false;

typedef std::vector<std::vector<int8_t>> grid2d_t;

class Grid
{
    grid2d_t m_Grid;
    std::vector<std::pair<int,int>> m_Checks;

    uint8_t at(int x, int y )
    {
        if( (x >= 0) && (x < 5) && (y >= 0) && (y < 5) )
            return m_Grid[y][x];
        else
            return 0;
    }

public:
    Grid( const std::string txt )
    {
        m_Grid.resize(5);
        for( int y = 0; y < 5; y++ ) {
            m_Grid[y].resize(5);
            for( int x = 0; x < 5; x++ )
                m_Grid[y][x] = txt[y*5+x] == '#';
        }

        //        for( ; *txt; txt++ )
        //            m_Grid.push_back( *txt == '#' );

        m_Checks.emplace_back( -1, 0 );
        m_Checks.emplace_back( 1, 0 );
        m_Checks.emplace_back( 0, -1 );
        m_Checks.emplace_back( 0, 1 );
    }

    grid2d_t & clone() {
        return m_Grid;
    }

    int rating()
    {
        int sum = 0;
        int i = 0;
        for( int y = 0; y < 5; y++ )
            for( int x = 0; x < 5; x++ )
                sum += m_Grid[y][x] << i++;

        return sum;
    }

    void cycle()
    {
        grid2d_t grid(5);
        for( int y = 0; y < 5; y++ )
        {
            grid[y].resize(5);
            for( int x = 0; x < 5; x++ )
            {
                int neighbors = std::accumulate( 
                    m_Checks.begin(), m_Checks.end(), 0,
                    [this,x,y](int i, std::pair<int,int> c)
                    { return i+at(x+c.first,y+c.second); }
                );

                grid[y][x] = neighbors == 1 ||  (neighbors == 2 && at(x,y) == 0);
            }
        }
        m_Grid = grid;
    }

    void print()
    {
        for( int y = 0; y < 5; y++ )
        {
            for( int x = 0; x < 5; x++ )
                std::cout << " " << ".#"[at(x,y)];
            std::cout <<"\n";
        }
    }
};


int part1(Grid & grid) {
    std::map<int,int> values;
    int r = grid.rating();
    values[r] = 0;

    for( int i = 1; ; i++ )
    {
        grid.cycle();
        r = grid.rating();
        if( DEBUG ) {
            grid.print();
            std::cout << i << " " << r << "\n";
        }
        if( values.find(r) != values.end() )
        {
            if( DEBUG )
                std::cout << r << "\n";
            break;
        }
        values[r] = i;
    }
    return r;
}


// Part 1 and part 2 really are very different.


//     |     |         |     |     
// 0,0 | 1,0 |   2,0   | 3,0 | 4,0 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,1 | 1,1 |   2,1   | 3,1 | 4,1 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |A|B|C|D|E|     |     
//     |     |-+-+-+-+-|     |     
//     |     |F|G|H|I|J|     |     
//     |     |-+-+-+-+-|     |     
// 0,2 | 1,2 |K|L|?|N|O| 3,2 | 4,2 
//     |     |-+-+-+-+-|     |     
//     |     |P|Q|R|S|T|     |     
//     |     |-+-+-+-+-|     |     
//     |     |U|V|W|X|Y|     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,3 | 1,3 |   2,3   | 3,3 | 4,3 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,4 | 1,4 |   2,4   | 3,4 | 4,4 
//     |     |         |     |     
//
//Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
//Tile G has four adjacent tiles: B, F, H, and L.
//Tile D has four adjacent tiles: 8, C, E, and I.
//Tile E has four adjacent tiles: 8, D, 14, and J.
//Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
//Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.

//  0,0 has 4:  (1,2,-1)  (2,1,-1)  (1,0,0)  (0,1,0)
//  1,0 has 4:  (0,0,0)   (2,1,-1)  (2,0,0)  (1,1,0)
//  2,0 has 4:  (1,0,0)   (2,1,-1)  (3,0,0)  (2,1,0)
//  3,0 has 4:  (2,0,0)   (2,1,-1)  (4,0,0)  (3,1,0)
//  4,0 has 4:  (3,0,0)   (2,1,-1)  (3,2,-1) (4,1,0)

//  0,1 has 4:  (1,2,-1)  (0,0,0)   (1,1,0)  (0,2,0)
//  1,1 has 4:  (0,1,0)   (1,0,0)   (2,1,0)  (1,2,0)
//  2,1 has 8:  (1,1,0)   (2,0,0)   (3,1,0)  (*,0,1)
//  3,1 has 4:  (2,1,0)   (3,0,0)   (4,1,0)  (3,2,0)
//  4,1 has 4:  (3,1,0)   (4,0,0)   (3,2,-1) (4,2,0)

//  0,2 has 4:  (1,2,-1)  (0,1,0)   (1,2,0)  (0,3,0)
//  1,2 has 8:  (0,2,0)   (1,1,0)   (0,*,0)  (1,2,0)
//  2,2 has 1:  (2,2,0)
//  3,2 has 8:  (4,*,0)   (3,1,0)   (4,2,0)  (3,3,0)
//  4,2 has 4:  (3,2,0)   (4,1,0)   (1,2,-1) (4,3,0)

//  0,3 has 4:  (1,2,-1)  (0,2,0)   (1,3,0)  (0,4,0)
//  1,3 has 4:  (0,1,0)   (1,2,0)   (2,3,0)  (1,4,0)
//  2,3 has 8:  (1,1,0)   (2,2,0)   (3,3,0)  (*,0,1)
//  3,3 has 4:  (2,1,0)   (3,2,0)   (4,3,0)  (3,4,0)
//  4,3 has 4:  (3,1,0)   (4,2,0)   (3,2,-1) (4,4,0)

//  0,4 has 4:  (1,2,-1)  (0,3,0)   (1,4,0)  (2,3,-1)
//  1,4 has 4:  (0,4,0)   (1,3,0)   (2,4,0)  (2,3,-1)
//  2,4 has 4:  (1,4,0)   (2,3,0)   (3,4,0)  (2,3,-1)
//  3,4 has 4:  (2,4,0)   (3,3,0)   (4,4,0)  (2,3,-1)
//  4,4 has 4:  (3,4,0)   (4,3,0)   (3,2,-1) (2,3,-1)

struct Point3 {
    int x;
    int y;
    int z;
};

#define fill {99,99,99},{99,99,99},{99,99,99},{99,99,99}

int rawcoords[5][5][8][3] = {
    //         W         N         E        S
    {
        { {1,2,-1}, {2,1,-1}, {1,0,0}, {0,1,0}, fill},
        { {0,0,0},  {2,1,-1}, {2,0,0}, {1,1,0}, fill},
        { {1,0,0},  {2,1,-1}, {3,0,0}, {2,1,0}, fill},
        { {2,0,0},  {2,1,-1}, {4,0,0}, {3,1,0}, fill},
        { {3,0,0},  {2,1,-1}, {3,2,-1},{4,1,0}, fill},
    },
    {
        { {1,2,-1}, {0,0,0},  {1,1,0}, {0,2,0}, fill},
        { {0,1,0},  {1,0,0},  {2,1,0}, {1,2,0}, fill},
        { {1,1,0},  {2,0,0},  {3,1,0},          {0,0,1}, {1,0,1}, {2,0,1}, {3,0,1}, {4,0,1}},
        { {2,1,0},  {3,0,0},  {4,1,0}, {3,2,0}, fill},
        { {3,1,0},  {4,0,0},  {3,2,-1},{4,2,0}, fill},
    },
    {
        { {1,2,-1}, {0,1,0},  {1,2,0}, {0,3,0}, fill},
        { {0,2,0},  {1,1,0},           {1,3,0}, {0,0,1}, {0,1,1}, {0,2,1}, {0,3,1}, {0,4,1}},
        { {2,2,0},                              fill, {99,99,99}, {99,99,99}, {99,99,99}},
        {           {3,1,0},  {4,2,0}, {3,3,0}, {4,0,1}, {4,1,1}, {4,2,1}, {4,3,1}, {4,4,1}}, 
        { {3,2,0},  {4,1,0},  {3,2,-1},{4,3,0}, fill},
    },
    {
        { {1,2,-1}, {0,2,0},  {1,3,0}, {0,4,0}, fill},
        { {0,3,0},  {1,2,0},  {2,3,0}, {1,4,0}, fill},
        { {1,3,0},            {3,3,0}, {2,4,0}, {0,4,1}, {1,4,1}, {2,4,1}, {3,4,1}, {4,4,1}},
        { {2,3,0},  {3,2,0},  {4,3,0}, {3,4,0}, fill},
        { {3,3,0},  {4,2,0},  {3,2,-1},{4,4,0}, fill},
    },
    {
        { {1,2,-1}, {0,3,0},  {1,4,0}, {2,3,-1}, fill},
        { {0,4,0},  {1,3,0},  {2,4,0}, {2,3,-1}, fill},
        { {1,4,0},  {2,3,0},  {3,4,0}, {2,3,-1}, fill},
        { {2,4,0},  {3,3,0},  {4,4,0}, {2,3,-1}, fill},
        { {3,4,0},  {4,3,0},  {3,2,-1},{2,3,-1}, fill},
    }
};


typedef std::vector<grid2d_t> grid3d_t;
typedef std::vector<std::vector<std::vector<Point3>>> coords_t;
coords_t coords;

coords_t convertCoords() {
    coords_t base;
    base.resize(5);
    for( int i = 0; i < 5; i++ ) {
        base[i].resize(5);
        for( int j = 0; j < 5; j++ ) {
            for( int k = 0; k < 8; k++ ) {
                if( rawcoords[i][j][k][0] < 99 ) {
                    base[i][j].push_back( Point3({
                        rawcoords[i][j][k][0],
                        rawcoords[i][j][k][1],
                        rawcoords[i][j][k][2]
                    }));
                }
            }
        }
    }
    return base;
}

// Makes a set of empty grids at the selected depth.

grid3d_t makegrids( int depth ) {
    grid3d_t grid(depth+1);
    for( int lvl = 0; lvl < depth+1; lvl++ )
    {
        grid[lvl].resize(5);
        for( int y = 0; y < 5; y++ )
        {
            grid[lvl][y].resize(5);
        }
    }
    return grid;
}


// Do another generation.

grid2d_t onelevel( const grid3d_t grid, int lvl ) {
    int depth = grid.size();
    grid2d_t newgrid(5);
    for( int y = 0; y < 5; y++ ) {
        newgrid[y].resize(5);
        for( int x = 0; x < 5; x++ ) {
            int nbrs = 0;
            for( auto p3d : coords[y][x] ) {
                if( (0 <= lvl+p3d.z) && (lvl+p3d.z < depth) ) {
                    nbrs += grid[lvl+p3d.z][p3d.y][p3d.x];
                }
            }
            if( nbrs == 1 || (nbrs == 2 && !grid[lvl][y][x])) 
                newgrid[y][x] = 1;
        }
    }
    return newgrid;
}

// This does all of the levels, one at a time.

grid3d_t doall( const grid3d_t & grid ) {
    grid3d_t newgrid(grid.size());
    for( int lvl = 0; lvl < grid.size(); lvl++ ) {
        newgrid[lvl] = onelevel(grid,lvl);
    }
    return newgrid;
}

int fancyrow( int depth, int start, int end, const grid3d_t & grids ) {
    if( DEBUG ) {
        for( int ii = start; ii < end; ii++ ) {
            std::cout << "    " << std::setw(4) << (ii-depth);
        }
        std::cout << "\n";
    }

    int sumx = 0;
    std::string s = "";
    for( int y = 0; y < 5; y++ ) {
        for( int lvl = start; lvl < end; lvl++ ) {
            s += "   ";
            for( int x = 0; x < 5; x ++ ) {
                s += ".#"[grids[lvl][y][x]];
                sumx += grids[lvl][y][x];
            }
        }
        s += "\n";
    }

    if( DEBUG )
        std::cout << s << "\n";

    return sumx;
}

int fancyprint( const grid3d_t & grid ) {
    int depth = grid.size() / 2;
    int sumx = 0;
    for( int i = 0; i < grid.size(); i += 10 )
        sumx += fancyrow( depth, i, std::min(i+10, int(grid.size())), grid );
    return sumx;
}

int part2( grid2d_t & center, int depth ) {
    grid3d_t grids = makegrids( depth );
    grids[depth/2] = center;
    for( int i = 0; i < depth; i++ ) {
        grids = doall(grids);
    }
    return fancyprint(grids);
}


int main( int argc, char ** argv )
{
    while( *++argv )
    {
        std::string arg(*argv);
        if( arg == "debug" )
            DEBUG = true;
        else if( arg == "test" )
            TEST = true;
    }

    int depth = TEST ? 10 : 200;

    coords = convertCoords();
    if( DEBUG )
        for( int y = 0; y < 5; y++ ) {
            for( int x = 0; x < 5; x++ )
            {
                for( auto & n : coords[y][x] )
                    std::cout << "(" << n.x << " " << n.y << " " << n.z << ") ";
                std::cout << "\n";
            }
            std::cout << "\n";
        }
    Grid grid( TEST ? test : input );
    std::cout << "Part 1: " << part1(grid) << "\n";
    Grid grid2( TEST ? test : input );
    std::cout << "Part 2: " << part2(grid2.clone(), depth) << "\n";
    return 0;
}
