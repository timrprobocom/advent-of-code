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
   "123 328  51 64 \n"
   " 45 64  387 23 \n"
   "  6 98  215 314\n"
   "*   +   *   +  "

);

#define DAY "day06"

bool DEBUG = false;
bool TEST = false;

typedef vector<vector<int64_t>> MatrixInt;

// Prep for part 1 by transposing the matrix.

MatrixInt transpose( const StringVector & data, const string & ops ) 
{
    MatrixInt cols(ops.size());
    for( auto & line : data )
    {
        vector<int> row = split_int( line );
        for( int i = 0; i < row.size(); i++ )
        {
            cols[i].push_back( row[i] );
        }
	}
    if( DEBUG )
    {
        for( auto & row : cols ) {
            for( auto n : row ) {
                cout << n << " ";
            }
            cout << "\n";
        }
    }
	return cols;
}

// Prep for part 2 by handling column by column.

MatrixInt transform(const StringVector & data, const string & ops)
{
    int ml = data[0].size();
    MatrixInt cols;
    vector<int64_t> col;
    for( int i = 0; i < ml; i++ )
    {
        int n = 0;
        for( auto & line : data ) 
            if( line[i] != ' ')
                n = n * 10 + line[i] - '0';
		
        if( n > 0 ) {
			col.push_back(n);
        }
		else if( !col.empty() )
        {
			cols.push_back( col );
			col.clear();
		}
	}
	
    if( !col.empty() )
        cols.push_back(col);

    if( DEBUG )
    {
        for( auto & row : cols ) {
            for( auto n : row ) {
                cout << n << " ";
            }
            cout << "\n";
        }
    }
	return cols;
}


int64_t part2 (const MatrixInt & nums, const string & ops )
{
    int64_t result = 0;
    for( int i = 0; i < ops.size(); i++ )
    {
        if( ops[i] == '*' )
            result += accumulate( nums[i].begin(), nums[i].end(), 1LL, multiplies<int64_t>() );
        else
            result += accumulate( nums[i].begin(), nums[i].end(), 0 );
    }
	return result;
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
    StringVector lines = split(input, "\n");
    string ops;
    
    for( auto c : lines.back() )
        if( c != ' ' )
            ops += c;

    lines.resize( lines.size() - 1 );
    
    cout << "Part 1: " << part2(transpose(lines,ops),ops) << "\n";
    cout << "Part 2: " << part2(transform(lines,ops),ops) << "\n";
}
