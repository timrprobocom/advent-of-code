#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <tuple>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;

const string test(
"0 3 6 9 12 15\n"
"1 3 6 10 15 21\n"
"10 13 16 21 30 45\n"
);


void parse( istream & data, vector<IntVector> & result )
{
    result.clear();
    string line;
    while( getline( data, line ) )
    {
        result.resize( result.size()+1 );
        istringstream parse(line);
        string word;
        while( parse >> word )
        {
            result.back().push_back(stoi(word));
        }
    }
}


int part1( int part, vector<IntVector> & result )
{
    int sumx = 0;
    for( auto & rowx : result )
    {
        IntVector row = rowx;
        vector<IntVector> stack;
        stack.push_back( row );

        // Determine differences.

        while( !equal( row.begin()+1, row.end(), row.begin() ) )
        {
            IntVector newrow;
            for( int i = 0; i < row.size()-1; i++ )
                newrow.push_back( row[i+1] - row[i] );
            row = newrow;
            stack.push_back( row );
        }

        int incr = 0;
        for( auto row = stack.rbegin(); row != stack.rend(); row++ )
        {
            incr = part == 1 ? (*row).back()+incr : (*row).front()-incr;
        }
        sumx += incr;
    }

    return sumx;
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

    vector<IntVector> data;
    if( TEST )
    {
        istringstream lines;
        lines.str(test);
        parse( lines, data );
    }
    else 
    {
        ifstream lines("day09.txt");
        parse( lines, data );
    }

    cout << "Part 1: " << part1(1, data) << "\n";
    cout << "Part 2: " << part1(2, data) << "\n";
}
