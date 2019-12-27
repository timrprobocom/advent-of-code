#include <iostream>
#include <fstream>
#include <vector>
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

bool TRACE = false;
bool TEST = false;

class Grid
{
    std::vector<uint8_t> m_Grid;
    std::vector<std::pair<int,int>> m_Checks;

    uint8_t at(int x, int y )
    {
        if( (x >= 0) && (x < 5) && (y >= 0) && (y < 5) )
            return m_Grid[y*5+x];
        else
            return 0;
    }

public:
    Grid( const std::string txt )
    {
        m_Grid.resize( txt.size() );
        std::transform( txt.begin(), txt.end(), m_Grid.begin(),
            [](char c) { return c == '#'; } );

//        for( ; *txt; txt++ )
//            m_Grid.push_back( *txt == '#' );

        m_Checks.emplace_back( -1, 0 );
        m_Checks.emplace_back( 1, 0 );
        m_Checks.emplace_back( 0, -1 );
        m_Checks.emplace_back( 0, 1 );
    }

    int rating()
    {
        int i = 0;
        return std::accumulate( m_Grid.begin(), m_Grid.end(), 0,
            [&i](int sum, uint8_t next) { return sum + (next << i++); } );
    }

    void cycle()
    {
        std::vector<uint8_t> grid;
        for( int y = 0; y < 5; y++ )
        {
            for( int x = 0; x < 5; x++ )
            {
                int neighbors = std::accumulate( 
                    m_Checks.begin(), m_Checks.end(), 0,
                    [this,x,y](int i, std::pair<int,int> c)
                    { return i+at(x+c.first,y+c.second); }
                );

                grid.push_back(
                    neighbors == 1 ||  (neighbors == 2 && at(x,y) == 0) 
                );
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


void main( int argc, char ** argv )
{
    while( *++argv )
    {
        if( strcmp( *argv, "trace" ) == 0 )
            TRACE = true;
        else if( strcmp( *argv, "test" ) == 0 )
            TEST = true;
    }

    Grid grid( TEST ? test : input );
    grid.print();
    int r = grid.rating();
    std::cout << grid.rating() << "\n";
    std::map<int, int> track;
    track[r] = 0;
    for( int i = 1; ; i++ )
    {
        grid.cycle();
        grid.print();
        r = grid.rating();
        std::cout << i << " " << r << "\n";
        if( track.find(r) != track.end() )
        {
            std::cout << "Part 1: " << i << " " << r << "\n";
            break;
        }
        track[r] = i;
    }
}
