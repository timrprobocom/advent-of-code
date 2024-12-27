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
"3   4\n"
"4   3\n"
"2   5\n"
"1   3\n"
"3   9\n"
"3   3"
);

bool DEBUG = false;
bool TEST = false;

int part1 (vector<int> & one, vector<int> & two )
{
    int sumx = 0;
    for( int i = 0; i < one.size(); i++ )
        sumx += abs(one[i]-two[i]);
    return sumx;
}

int part2 (vector<int> & one, vector<int> & two )
{
    int sumx = 0;
    for( int i = 0; i < one.size(); i++ )
        sumx += one[i] * count(two.begin(), two.end(), one[i] );
    return sumx;
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


    stringstream input;
    if( TEST )
        input << test;
    else
        input << ifstream("day01.txt").rdbuf();

    vector<int> data{
        istream_iterator<int>(input),
        istream_iterator<int>()
    };

    vector<int> one;
    vector<int> two;
    for( int i = 0; i < data.size(); i+=2 )
    {
        one.push_back( data[i] );
        two.push_back( data[i+1] );
    }
    sort( one.begin(), one.end() );
    sort( two.begin(), two.end() );

    cout << "Part 1: " << part1(one,two) << "\n";
    cout << "Part 2: " << part2(one,two) << "\n";
}
