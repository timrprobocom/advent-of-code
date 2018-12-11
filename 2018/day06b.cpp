#include <iostream>
#include <fstream>
#include <vector>

struct point_t {
    int x;
    int y;
};

int test[][2] = {
    {1, 1},
    {1, 6},
    {8, 3},
    {3, 4},
    {5, 5},
    {8, 9}
};

void readlive( std::vector<point_t> & inx )
{
    std::ifstream ifs( "day06.txt" );
    point_t pt;
    while( ifs )
    {
        ifs >> pt.x >> pt.y;
        if( !ifs ) break;
        inx.push_back( pt );
    }
}

int ham( int x0, int y0, int x1, int y1 )
{
    return abs(x1-x0)+abs(y1-y0);
}

#define TARGET 10000

int main()
{
    std::vector<point_t> live;

    readlive( live );

    int knt = 0;
    for( int y = -12000; y < 12000; y++ )
    {
        std::cout << y << '\r' << std::flush;
        for( int x = -12000; x < 12000; x++ )
        {
            int sumh = 0;
            for( auto && pt : live )
            {
                sumh += ham( x, y, pt.x, pt.y );
                if( sumh >= TARGET )
                    break;
            }
            if( sumh < TARGET )
            {
                std::cout << x << "," << y << "\n";
                knt += 1;
            }
        }
    }

    std::cout << "\n" << knt << "\n";
}
