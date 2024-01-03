#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;

const char * test1 = 
"1abc2\n"
"pqr3stu8vwx\n"
"a1b2c3d4e5f\n"
"treb7uchet\n";

const char * test2 = 
"two1nine\n"
"eightwothree\n"
"abcone2threexyz\n"
"xtwone3four\n"
"4nineeightseven2\n"
"zoneight234\n"
"7pqrstsixteen\n";

const string nums[] = {
    "***",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
};



int part1( istringstream & data )
{
    int sum = 0;
    string line;
    while( getline( data, line ) )
    {
        int d1 = -1, d2 = -1;
        for( char c : line )
        {
            if( isdigit(c) )
                d2 = c - '0';
                if( d1 < 0 )
                    d1 = d2;
        }
        sum += d1*10+d2;
    }
    return sum;
}

int part2( istringstream & data )
{
    int sum = 0;
    string line;
    while( getline( data, line ) )
    {
        int d1 = -1, d2 = -1;
        for( int i = 0; i < line.size(); i++ )
        {
            if( isdigit(line[i]) )
            {
                d2 = line[i] - '0';
            }
            else {
                for( int j = 0; j < 10; j++ )
                {
                    int len = nums[j].size();
                    if( (i + len <= line.size()) && line.substr(i,len) == nums[j] )
                    {
                        d2 = j;
                        i += len - 2;
                        break;
                    }
                }
            }
            if( d2 >=0 && d1 < 0 )
                d1 = d2;
        }
        sum += d1*10+d2;
    }
    return sum;
}


int main( int argc, char ** argv )
{
    istringstream data1;
    istringstream data2;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
        {
            data1.str( test1 );
            data2.str( test2 );
        }
    }

    if( data1.str().empty() )
    {
        stringstream buffer;
        buffer << ifstream("day01.txt").rdbuf();
        data1.str( buffer.str() );
        data2.str( buffer.str() );
    }

    cout << "Part 1: " << part1(data1) << "\n";
    cout << "Part 2: " << part2(data2) << "\n";
}



