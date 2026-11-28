#include <iostream>
#include <fstream>
#include <vector>

bool DEBUG = false;

int SQ = 360;
int TARGET = 10000;
int MAXD = 500;

struct point_t {
    int x;
    int y;
};

typedef std::vector<point_t> pointlist_t;
typedef std::vector<std::vector<int>> matrix_t;

int test[][2] = {
    {1, 1},
    {1, 6},
    {8, 3},
    {3, 4},
    {5, 5},
    {8, 9}
};

void readlive( pointlist_t & inx )
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

int hamming( int x0, int y0, int x1, int y1 )
{
    return abs(x1-x0)+abs(y1-y0);
}


// Create a square grid of size sq containing -1.

matrix_t create( int sq, pointlist_t & data )
{
    matrix_t mat(sq, std::vector<int>(sq, -1));
    for( int i = 0; i < data.size(); i++ )
        mat[data[i].y][data[i].x] = i;
    return mat;
}

void update( matrix_t & mat, pointlist_t & data )
{
    for( int y = 0; y < SQ; y++ ) {
        for( int x = 0; x < SQ; x++ ) {
            int mind = 9999;
            std::vector<int> minxy;
            for( int i = 0; i < data.size(); i++ ) {
                point_t pt = data[i];
                int dist = hamming( x, y, pt.x, pt.y );
                if( dist == mind ) {
                    minxy.push_back( i );
                } else if( dist < mind ) {
                    mind = dist;
                    minxy.clear();
                    minxy.push_back( i );
                }
            }
            if( minxy.size() == 1 ) {
                mat[y][x] = minxy[0];
            }
        }
    }
}

int part1( pointlist_t & data )
{
    std::vector<std::vector<int>> mat = create(SQ, data);
    update( mat, data );
    std::vector<int> tots(data.size());
    for( int y = 0; y < SQ; y++ ) 
        for( int x = 0; x < SQ; x++ ) 
            if( mat[y][x] >= 0  )
                tots[mat[y][x]] ++;

    for( int n = 0; n < SQ; n++ ) 
    {
        if( mat[n][0] >= 0)    tots[mat[n][0]] = 0;
        if( mat[n][SQ-1] >= 0) tots[mat[n][SQ-1]] = 0;
        if( mat[0][n] >= 0)    tots[mat[0][n]] = 0;
        if( mat[SQ-1][n] >= 0) tots[mat[SQ-1][n]] = 0;
    }
    return *std::max_element( tots.begin(), tots.end() );
}

int part2( pointlist_t & data ) 
{
    int knt = 0;
    for( int y = -MAXD; y < MAXD; y++ )
    {
        if( DEBUG )
            std::cout << y << '\r' << std::flush;
        for( int x = -MAXD; x < MAXD; x++ )
        {
            int sumh = 0;
            for( auto && pt : data )
            {
                sumh += hamming( x, y, pt.x, pt.y );
                if( sumh >= TARGET )
                    break;
            }
            if( sumh < TARGET )
            {
                if( DEBUG )
                    std::cout << x << "," << y << "\n";
                knt += 1;
            }
        }
    }

    return knt;
}

int main()
{
    std::vector<point_t> live;

    readlive( live );

    std::cout << "Part 1: " << part1(live) << "\n";
    std::cout << "Part 2: " << part2(live) << "\n";
}
