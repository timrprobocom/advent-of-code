#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"p=0,4 v=3,-3\n"
"p=6,3 v=-1,-3\n"
"p=10,3 v=-1,2\n"
"p=2,0 v=2,-1\n"
"p=0,0 v=1,3\n"
"p=3,0 v=-2,-2\n"
"p=7,6 v=-1,-3\n"
"p=3,0 v=-1,-2\n"
"p=9,3 v=2,3\n"
"p=7,3 v=-1,2\n"
"p=2,4 v=2,-3\n"
"p=9,5 v=-3,-3"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day14"

int WIDTH=-1;
int HEIGHT=-1;

void printgrid(IntMatrix & data)
{
    uint8_t grid[HEIGHT][WIDTH] = {0};
    bzero( grid, WIDTH*HEIGHT );
    for( auto & bot : data )
        grid[bot[1]][bot[0]] += 1;
    for( int y=0; y < HEIGHT; y++ )
    {   
        for( int x=0; x < WIDTH; x++ )
            cout << ".1234"[grid[y][x]];
        cout << endl;
    }
}

void move(IntMatrix & data)
{
    for( auto & row : data )
    {
        row[0] = (row[0] + row[2] + WIDTH) % WIDTH;
        row[1] = (row[1] + row[3] + HEIGHT) % HEIGHT;
    }
}

int64_t part1(IntMatrix & data)
{
    for( int i = 0; i < 100; i++ )
        move(data);

    int hw = WIDTH/2;
    int hh = HEIGHT/2;
    int k[4] = {0,0,0,0};
    for( auto & row : data )
    {
        if( row[0] < hw && row[1] < hh )
            k[0]++;
        if( row[0] > hw && row[1] < hh )
            k[1]++;
        if( row[0] < hw && row[1] > hh )
            k[2]++;
        if( row[0] > hw && row[1] > hh )
            k[3]++;
    }
    return k[0]*k[1]*k[2]*k[3]; 
}

// The tree is solid, so the standard deviation of the coordinates goes WAY down.
// Tpyical is 30, tree gets 19.

bool detect_tree( IntMatrix & data )
{
    int n = data.size();
    float sumx = 0;
    float sumx2 = 0;
    float sumy = 0;
    float sumy2 = 0;
    for( auto & row : data )
    {
        sumx += row[0];
        sumx2 += row[0]*row[0];
        sumy += row[1];
        sumy2 += row[1]*row[1];
    }
    float meanx = sumx / n;
    float meany = sumy / n;
    float stdx = sqrt((sumx2 / n) - (meanx * meanx));
    float stdy = sqrt((sumy2 / n) - (meany * meany));

    return stdx < 20 && stdy < 20;
}  


int64_t part2(IntMatrix & data)
{
    for( int i = 100; i < 10000; i++ )
    {
        move(data);
        if( detect_tree(data) )
        {
            if( DEBUG )
                printgrid(data);
            return i+1;
        }
    }
    return 0;
}


int main( int argc, char ** argv )
{
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    string input = TEST ? test : file_contents(DAY".txt");
    if( TEST )
    {
        WIDTH = 11;
        HEIGHT = 7;
    }
    else
    {
        WIDTH = 101;
        HEIGHT = 103;
    }

    // For parsing, each line has four numbers, possibly with a sign.

    IntMatrix data(1);
    int accum = 0;
    int state = 0;
    for( char c : input )
    {
        if( c == '-' )
        {
            state = -1;
        }
        else if( isdigit(c) )
        {
            if( !state )
                state = 1;
            accum = accum * 10 + c - '0';
        }
        else
        {
            if( state )
            {
                data.back().push_back( accum * state );
                accum = 0;
                state = 0;
            }
            if( c == '\n' )
                data.push_back( vector<int>() );
        }
    }

    if( accum )
        data.back().push_back(accum * state);

    cout << "Part 1: " << part1(data) << "\n";
    if( DEBUG )
        printgrid( data );
    if( !TEST )
        cout << "Part 2: " << part2(data) << "\n";
}