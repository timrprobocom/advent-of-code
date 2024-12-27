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
"7 6 4 2 1\n"
"1 2 7 8 9\n"
"9 7 6 2 1\n"
"1 3 2 4 5\n"
"8 6 4 4 1\n"
"1 3 6 7 9"
);

bool DEBUG = false;
bool TEST = false;

bool is_safe( vector<int> & row )
{
    for( int i = 0; i < row.size()-1; i++ )
    {
        int x = row[i];
        int y = row[i+1];
        if( (y-x) * (row[1]-row[0]) < 0 )
            return false;
        if( abs(y-x) < 1 || abs(y-x) > 3 )
            return false;
    }
    return true;
}

int part1( IntMatrix data )
{
    int sumx = 0;
    for( auto & row : data )
       sumx += is_safe(row);
    return sumx;
}

int part2( IntMatrix data )
{
    int safe = 0;
    for( auto & row : data )
    {
        if( is_safe(row) )
        {
            safe += 1;
        }
        else
        {
            for( int i=0; i < row.size(); i++ )
            {
                vector<int> newrow = row;
                newrow.erase( newrow.begin()+i );
                if( is_safe(newrow) )
                {
                    safe += 1;
                    break;
                }
            }
        }
    }
    return safe;
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


    string input = TEST ? test : file_contents("day02.txt");
    StringVector lines = split(input, "\n");
    // Not strictly a matrix, since the rows are of different lengths.
    IntMatrix data;
    for( auto & row : lines )
    {
        stringstream ss(row);
        data.push_back( vector<int>(
            istream_iterator<int>(ss),
            istream_iterator<int>()
        ));
    }


    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
