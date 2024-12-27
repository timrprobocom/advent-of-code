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
"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
);

bool DEBUG = false;
bool TEST = false;

int part1( string & data )
{
    int sumx = 0;
    int i = 0;
    for( i = 0; i < data.size(); i++ )
    {
        if( data.substr(i,4) == "mul(" )
        {
            i += 4;
            int a = 0;
            int b = 0;
            for( ; isdigit(data[i]); i++)
                a = a * 10 + data[i] - '0';
            if( data[i] != ',' )
                continue;
            for( i++ ; isdigit(data[i]); i++)
                b = b * 10 + data[i] - '0';
            if( data[i] != ')' )
                continue;
            sumx += a * b;
        }
    }
    return sumx;
}

int part2( string & data )
{
    int sumx = 0;
    int i = 0;
    bool yes = true;
    for( i = 0; i < data.size(); i++ )
    {
        if( data.substr(i,4) == "do()" )
        {
            yes = true;
        }
        else if( data.substr(i,7) == "don't()" )
        {
            yes = false;
        }
        else if( yes && data.substr(i,4) == "mul(" )
        {
            i += 4;
            int a = 0;
            int b = 0;
            for( ; isdigit(data[i]); i++)
                a = a * 10 + data[i] - '0';
            if( data[i] != ',' )
                continue;
            for( i++ ; isdigit(data[i]); i++)
                b = b * 10 + data[i] - '0';
            if( data[i] != ')' )
                continue;
            sumx += a * b;
        }
    }
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

    string input = TEST ? test : file_contents("day03.txt");

    cout << "Part 1: " << part1(input) << "\n";
    cout << "Part 2: " << part2(input) << "\n";
}
