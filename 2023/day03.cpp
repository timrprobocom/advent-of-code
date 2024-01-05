#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <array>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;

const char * test1 = 
"467..114..\n"
"...*......\n"
"..35..633.\n"
"......#...\n"
"617*......\n"
".....+.58.\n"
"..592.....\n"
"......755.\n"
"...$.*....\n"
".664.598.."
;

typedef vector<string> StringVector;

int W = 0;
int H = 0;

struct Number {
    int x;
    int y;
    int v;
    int l;
};

typedef vector<Number> NumberVector;

struct Point {
    int x;
    int y;
};

typedef vector<Point> PointVector;

bool OK(char c)
{
    return isdigit(c) || c == '.';
}

void parse( StringVector & data, NumberVector & nums, PointVector & syms )
{
    nums.clear();
    syms.clear();
    for( int y = 0; y < data.size(); y++ )
    {
        string row = data[y];
        bool num = false;
        for( int x = 0; x < row.size(); x++ )
        {
            char c = row[x];
            if( isdigit(c) )
            {
                if( !num )
                    nums.push_back(Number({x,y,0,0}));
                nums.back().v = nums.back().v * 10 + c - '0';
                nums.back().l += 1;
            }
            else if( c != '.') 
            {
                syms.push_back(Point({x,y}));
            }
            num = isdigit(c);
        }
    }
}

int part2( int part, NumberVector & numbers, PointVector & symbols )
{
    int sumx = 0;
    vector<int> nums;

    for( auto & sym : symbols )
    {
        nums.clear();
        for( auto & num : numbers )
        {
            if(
                num.y-1 <= sym.y && sym.y <= num.y+1 &&
                num.x-1 <= sym.x && sym.x <= num.x+num.l
            )
            {
                nums.push_back( num.v );
            }
        }

        if( part == 1 )
        {
            sumx += accumulate(nums.begin(), nums.end(), 0);
        }
        else if(nums.size() == 2)
        {
            int p = 1;
            for( auto n : nums )
                p *= n;
            sumx += p;
        }            
    }
    return sumx;
}

void splitem( istream & is, StringVector & lines )
{
    string line;
    while( getline( is, line ) )
        lines.push_back( line );  
}

int main( int argc, char ** argv )
{
    bool TEST = false;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    StringVector data;
    if( TEST )
    {
        istringstream iss;
        iss.str( test1 );
        splitem( iss, data );
    }
    else
    {
        ifstream ifs("day03.txt");
        splitem( ifs, data );
    }

    NumberVector numbers;
    PointVector symbols;
    parse( data, numbers, symbols );

    cout << "Part 1: " << part2(1,numbers,symbols) << "\n";
    cout << "Part 2: " << part2(2,numbers,symbols) << "\n";
}


