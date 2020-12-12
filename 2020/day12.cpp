#include <fstream>
#include <iostream>
#include <map>
#include <array>
#include <string>
#include <vector>
#include <algorithm>

#include "utils.h"

using namespace std;

array<string,5> test = { "F10", "N3", "F7", "R90", "F11" };

map<char,Point> deltas;

string directions( "NESW" );

// N and E are negative.


int part1(vector<string> & data)
{
    Point ship(0,0);
    Point facing = deltas['E'];

    for( auto && ln : data ) 
    {
        char direc = ln[0];
        int dist = stoi(ln.substr(1));
        if( directions.find(direc) != directions.npos )
        {
            ship += deltas[direc] * dist;
        }
        else if( direc == 'L' )
        {
            int count = dist / 90;
            for( int i = 0; i < count; i++ )
                facing.left();
        }
        else if( direc == 'R' )
        {
            int count = dist / 90;
            for( int i = 0; i < count; i++ )
                facing.right();
        }
        else if( direc == 'F' )
        {
            ship += facing * dist;
        }
#if DEBUG
        cout << ln << ship << "\n";
#endif
    }
    return ship.mandist();
}


int part2(vector<string> & data)
{
    Point ship(0,0);
    Point waypt(10,-1);

    for( auto && ln : data ) 
    {
        char direc = ln[0];
        int dist = stoi(ln.substr(1));
        if( directions.find(direc) != directions.npos )
        {
            waypt += deltas[direc] * dist;
        }
        else if( direc == 'L' )
        {
            int count = dist / 90;
            for( int i = 0; i < count; i++ )
                waypt.left();
        }
        else if( direc == 'R' )
        {
            int count = dist / 90;
            for( int i = 0; i < count; i++ )
                waypt.right();
        }
        else if( direc == 'F' )
        {
            ship += waypt * dist;
        }
#ifdef DEBUG
        cout << ln << ship << "\n";
#endif
    }
    return ship.mandist();
}


int main()
{
    deltas['N'] = Point( 0,-1);
    deltas['E'] = Point( 1, 0);
    deltas['S'] = Point( 0, 1);
    deltas['W'] = Point(-1, 0);

    vector<string> data;
#ifdef TEST
    copy( test.begin(), test.end(), back_inserter(data) );
#else
    ifstream ifs( "day12.txt" );
    for( string line; getline(ifs, line); )
        data.push_back( line );
#endif

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}

