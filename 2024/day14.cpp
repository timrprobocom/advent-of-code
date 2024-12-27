#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <queue>
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

int WIDTH = -1;
int HEIGHT = -1;

typedef vector<vector<int>> IntMatrix;

void printdata( IntMatrix & data )
{
    for( auto & row : data )
    {
        cout << row[0] << " " << row[1] << " " << row[2] << " " << row[3] << "\n";
    }
}


void printgrid( IntMatrix & data )
{
    vector<string> grid;
    for( int i = 0; i < HEIGHT; i++ )
        grid.push_back( string(WIDTH, '0') );
    for( auto & row : data )
        grid[row[1]][row[0]] ++;
    for( auto & row : grid )
        cout << row << "\n";
}


void move( IntMatrix & data )
{
    for( auto & row : data )
    {
        row[0] = (row[0] + row[2] + WIDTH) % WIDTH;
        row[1] = (row[1] + row[3] + HEIGHT) % HEIGHT;
    }
}


double calculateStandardDeviation(const vector<int> & arr)
{
    double sum = 0.0, mean = 0.0, standardDeviation = 0.0;

    int size = arr.size();

    // Calculate the sum of elements in the vector.

    for( auto n : arr )
        sum += n;

    // Calculate the mean

    mean = sum / size;

    // Calculate the sum of squared differences from the mean.

    for( auto n : arr )
        standardDeviation += (n-mean) * (n-mean);

    // Calculate the square root of the variance to get the
    // standard deviation

    return sqrt(standardDeviation / size);
}


// The tree is solid, so the standard deviation of the coordinates goes WAY down.
// Typical is 30, tree gets 19.

bool detect_tree( IntMatrix & data )
{
    vector<int> column;
    for( int i = 0; i < 2; i++ )
    {
        transform( 
            data.begin(),
            data.end(),
            back_inserter( column ),
            [i]( vector<int> & row ) { return row[i]; }
        );

        double x = calculateStandardDeviation(column);
        if( x > 24.0 )
            return false;
    }
    if( DEBUG )
        printgrid(data);
    return true;
}


int64_t part1( IntMatrix & data )
{
    for( int i = 0; i < 100; i++ )
        move( data );

    int hw = WIDTH/2;
    int hh = HEIGHT/2;
    int k1=0, k2=0, k3=0, k4=0;
    for( auto & row : data )
    {
        if( row[0] < hw )
        {
            if( row[1] < hh )
                k1++;
            else if( row[1] > hh )
                k2++;
        }
        else if( row[0] > hw )
        {
            if( row[1] < hh )
                k3++;
            else if( row[1] > hh )
                k4++;
        }
    }

    return k1*k2*k3*k4;
}

int64_t part2( IntMatrix & data )
{
    for( int i = 101; i < 10000; i++ )
    {
        move( data );
        if( detect_tree(data) )
            return i;
    }
    return -1;
}

int main( int argc, char ** argv )
{
    string name = *argv;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

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

    string input = TEST ? test : file_contents("day14.txt");

    IntMatrix data(1);
    int sign = 1;
    int accum = 0;
    bool more = false;
    for( char c : input )
    {
        if( c == '-' )
        {
            sign = -1;
        }
        else if( '0' <= c && c  <= '9' )
        {
            accum = accum * 10 + (c - '0');
            more = true;
        }
        else if( more )
        {
            data.back().push_back( sign*accum );
            sign = 1;
            accum = 0;
            more = false;
            if( c == '\n' )
                data.push_back( vector<int>() );
        }
    }
    data.back().push_back( sign*accum );

    cout << "Part 1: " << part1(data) << "\n";
    if( !TEST )
        cout << "Part 2: " << part2(data) << "\n";
}
