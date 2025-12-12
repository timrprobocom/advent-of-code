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
"0:\n"
"###\n"
"##.\n"
"##.\n"
"\n"
"1:\n"
"###\n"
"##.\n"
".##\n"
"\n"
"2:\n"
".##\n"
"###\n"
"##.\n"
"\n"
"3:\n"
"##.\n"
"###\n"
"##.\n"
"\n"
"4:\n"
"###\n"
"#..\n"
"###\n"
"\n"
"5:\n"
"###\n"
".#.\n"
"###\n"
"\n"
"4x4: 0 0 0 0 2 0\n"
"12x5: 1 0 1 0 2 2\n"
"12x5: 1 0 1 0 3 2"
);

#define DAY "day12"

bool DEBUG = false;
bool TEST = false;


int64_t part1 ( IntMatrix & numbers )
{
    int count = 0;
    for( auto & row : numbers )
    {
        int area = row[0] * row[1];
        int need = accumulate( row.begin()+2, row.end(), 0 ) * 8;
        count += area > need;
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
    auto data = split(input);
    IntMatrix numbers;
    for( auto & line : data ) 
    {
        if( line.find('x') == line.npos )
            continue;
        auto parts = split(line, " ");
        vector<int> row;
        auto q = split(parts[0], "x");
        row.push_back( stoi(q[0]) );
        row.push_back( stoi(q[1]) );
        for( int i = 1; i < parts.size(); i++ )
            row.push_back( stoi(parts[i]) );
        numbers.push_back( row );
    }
    
    cout << "Part 1: " << part1(numbers) << "\n";
}
