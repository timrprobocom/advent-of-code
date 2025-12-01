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
    "L68\n"
    "L30\n"
    "R48\n"
    "L5\n"
    "R60\n"
    "L55\n"
    "L1\n"
    "L99\n"
    "R14\n"
    "L82"
);

#define DAY "day01"

bool DEBUG = false;
bool TEST = false;

int part1 (StringVector & data )
{
    int count = 0;
    int pos = 50;
    for( auto & line : data )
    {
        int c = std::stoi( line.substr( 1 ) );
        if( line[0] == 'L' )
            pos = (pos - c + 100) % 100;
        else
            pos = (pos + c) % 100;
        count += !pos;
    }
    return count;
}

int part2 (StringVector & data)
{
    int count = 0;
    int pos = 50;
    for( auto & line : data )
    {
        int c = std::stoi( line.substr( 1 ) );
        if( line[0] == 'L' )
        {
            count -= !pos;
            pos -= c;
            while( pos < 0 )
            {
                count++;
                pos += 100;
            }
            count += !pos;
        }            
        else
        {
            pos += c;
            count += pos / 100;
            pos %= 100;
        }
    }
    return count;
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

    string input = TEST ? test : file_contents(DAY".txt");
    StringVector data = split(input);
    
    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
