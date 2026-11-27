#include <iostream>
#include <algorithm>
#include <vector>
bool TRACE = false;
bool TEST = false;
bool DEBUG = false;
#include "intcode.h"

#define __countof(x)    (sizeof(x)/sizeof(x[0])

std::vector<int> t1 = {3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0};  // 43210
std::vector<int> t2 = {3,23,3,24,1002,24,10,24,1002,23,-1,23, 101,5,23,23,1,24,23,23,4,23,99,0,0}; // 54321
std::vector<int> t3 = {3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0}; // 365210


std::vector<int> live = { 3,8,1001,8,10,8,105,1,0,0,21,38,55,80,97,118,199,280,361,442,99999,3,9,101,2,9,9,1002,9,5,9,1001,9,4,9,4,9,99,3,9,101,5,9,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1001,9,4,9,102,5,9,9,101,4,9,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,3,9,9,4,9,99,3,9,101,5,9,9,1002,9,2,9,101,3,9,9,1002,9,5,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99};


int part1( std::vector<int> & code )
{
    int maxval = 0;
    std::vector<int> inputset = { 0,1,2,3,4 };
    do
    {
        if( DEBUG ) {
            for( auto ip : inputset )
                std::cout << ip;
            std::cout << "\n";
        }
        int lastval = 0;
        for( auto ip : inputset )
        {
            Program<int>pgm( code );
            pgm.push( ip );
            pgm.push( lastval );
            pgm.run();
            lastval = pgm.pop();
            if( TRACE )
                std::cout << lastval << "\n";
        }
        maxval = std::max(maxval,lastval);
    }
    while( std::next_permutation( inputset.begin(), inputset.end() ));
    return maxval;
}

    

int part2( std::vector<int> &program ) {
    int maxval = 0;
    std::vector<int> inputset = { 5,6,7,8,9 };
    int lastval = 0;
    do
    {
        std::vector<Program<int>> amps;
        for( int i = 0; i < 5; i++ ) {
            amps.emplace_back( program );
        }

        // The output from 0 sends to the input of 1.

        Program<int>::connect( amps[0], amps[1] );
        Program<int>::connect( amps[1], amps[2] );
        Program<int>::connect( amps[2], amps[3] );
        Program<int>::connect( amps[3], amps[4] );
        Program<int>::connect( amps[4], amps[0] );

        // Set the initial phase input for each amp.

        for( int i = 0; i < 5; i++ )
            amps[i].push( inputset[i] );

        // Set the first signal into amp 0.

        amps[0].push( 0 );

        // Go.

        for( auto & amp : amps )
            amp.start();

        // Wait for the chain to exit.

        for( auto & amp : amps )
            amp.wait();

        // The answer is waiting in amp 4's output queue.

        maxval = std::max( maxval, amps[4].Final() );
    }
    while( std::next_permutation( inputset.begin(), inputset.end() ));

    return maxval;
}

int main( int argc, char ** argv )
{
    while( *++argv )
    {
        std::string s(*argv);
        if( s == "trace" )
            TRACE = true;
        else if( s == "test" )
            TEST = true;
        else if( s == "debug" )
            DEBUG = true;
    }
    std::vector<int> & data = TEST ? t3 : live;
    std::cout << "Part 1: " << part1(data) << "\n";
    std::cout << "Part 2: " << part2(data) << "\n";
}
