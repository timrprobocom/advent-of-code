#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"Button A: X+94, Y+34\n"
"Button B: X+22, Y+67\n"
"Prize: X=8400, Y=5400\n"
"\n"
"Button A: X+26, Y+66\n"
"Button B: X+67, Y+21\n"
"Prize: X=12748, Y=12176\n"
"\n"
"Button A: X+17, Y+86\n"
"Button B: X+84, Y+37\n"
"Prize: X=7870, Y=6450\n"
"\n"
"Button A: X+69, Y+23\n"
"Button B: X+27, Y+71\n"
"Prize: X=18641, Y=10279\n"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day13"


#define IN
#define OUT
#define INOUT

// We use LAPACK's sgesv_ for singles, dgesv_ for doubles.
//
// sgesv_ is a symbol in the LAPACK library files for solving systems 
// of linear equations.  Note that the arrays must be column-major.
// Also, Fortran is strictly pass by reference, which is why 
// everything here is a pointer.

extern "C" int dgesv_(
     IN  int * N,       // number of equations (3)
     IN  int * NRHS,    // number of right-hand sides (1)
   INOUT double * A,
     IN  int * LDA,     // leading dimension of A
     OUT int * IPIV,    // pivot indexes 
   INOUT double * B,    // RHS in, result out
     IN  int * LDB,     // leading dimension of B
     OUT int * info     // success/fail code, 0=OK
);


int64_t part1(vector<vector<int>> & data )
{
    int sumx = 0;
    for( auto game : data )
    {
        int ax = game[0];
        int ay = game[1];
        int bx = game[2];
        int by = game[3];
        int px = game[4];
        int py = game[5];

        for( int a = 1; a < px/ax; a++ )
        {
            if( (px - a * ax) % bx == 0 )
            {
                int b = (px - a * ax) / bx;
                if( ay*a + by*b == py )
                {
                    sumx += a * 3 + b;
                    break;
                }
            }
        }
    }
    return sumx;
}

// This can be used to solve part 1 as well, by passing 0.

int64_t part2(vector<vector<int>> & data, int64_t offset = 10000000000000)
{
    int64_t sumx = 0;
    for( auto game : data )
    {
        int ax = game[0];
        int ay = game[1];
        int bx = game[2];
        int by = game[3];
        int64_t px = game[4] + offset;
        int64_t py = game[5] + offset;

        // We are setting up the equations:
        //   ax*x + bx*x = px
        //   ay*x + by*x = py

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wnarrowing"
        double sys[] = { ax, ay, bx, by };
        double equals[] = { px, py };
#pragma GCC diagnostic pop

        // Set up the call to LAPACK dgesv.

        int N = 2;
        int NRHS = 1;
        int LDA = 2;
        int IPIV[2];
        int LDB = 2;
        int info;
        dgesv_( &N, &NRHS, sys, &LDA, IPIV, equals, &LDB, &info );

        // If the solution is not integral, there is no solution.

        int64_t a = equals[0] + 0.5;
        int64_t b = equals[1] + 0.5;
        if( a*ax+b*bx == px && a*ay+b*by == py )
        {
            sumx += a *3 + b;
        }
    }
    return sumx;
};


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

    string input = TEST ? test : file_contents(DAY".txt");

    // For parsing, each line has two numbers, possibly with a sign.  We find them.
    // A blank line ends a set of six.

    vector<vector<int>> data(1);
    for( auto & line : split(input) )
    {
        if( line.empty() )
        {
            data.push_back( vector<int>() );
            continue;
        }
        auto x = line.find('X');
        auto y = line.find('Y');
        if( line[x+1] == '=' )
        {
            data.back().push_back( stoi(line.substr(x+2)) );
            data.back().push_back( stoi(line.substr(y+2)) );
        }
        else
        {
            data.back().push_back( stoi(line.substr(x+1)) );
            data.back().push_back( stoi(line.substr(y+1)) );
        }
    }
    if( data.back().empty() )
        data.resize( data.size() - 1 );


    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 1: " << part2(data,0) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
