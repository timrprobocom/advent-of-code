#include <iostream>
#include <fstream>
#include <map>
#include <array>
#include <vector>

using namespace std;

array<int,7> live {0,20,7,16,1,18,15};

bool DEBUG = false;

// Given the starting numbers 0,3,6, the 2020th number spoken is 465.
// Given the starting numbers 1,3,2, the 2020th number spoken is 1.
// Given the starting numbers 2,1,3, the 2020th number spoken is 10.
// Given the starting numbers 1,2,3, the 2020th number spoken is 27.
// Given the starting numbers 2,3,1, the 2020th number spoken is 78.
// Given the starting numbers 3,2,1, the 2020th number spoken is 438.
// Given the starting numbers 3,1,2, the 2020th number spoken is 1836.

// Given 0,3,6, the 30000000th number spoken is 175594.
// Given 1,3,2, the 30000000th number spoken is 2578.
// Given 2,1,3, the 30000000th number spoken is 3544142.
// Given 1,2,3, the 30000000th number spoken is 261214.
// Given 2,3,1, the 30000000th number spoken is 6895259.
// Given 3,2,1, the 30000000th number spoken is 18.
// Given 3,1,2, the 30000000th number spoken is 362.


int run( vector<int> & data, int count )
{
    vector<int> found( count, -1 );
    for( int i = 0; i < data.size()-1; i++ )
        found[data[i]] = i+1;

    int nextx = data.back();

    for( int tape = data.size(); tape < count; tape++ )
    {
        int lastx = found[nextx] < 0 ? tape : found[nextx];
        found[nextx] = tape;
        nextx = tape - lastx;
    }

    return nextx;
}

int main( int argc, char ** argv )
{
    vector<int> data;

    while( *++argv )
    {
        if( strcmp( *argv, "debug" ) == 0 )
            DEBUG = true;
        else
            data.push_back( atoi(*argv) );
    }

    if( data.empty() )
        copy( live.begin(), live.end(), back_inserter(data) );

    cout << "Pass 1:" << run(data, 2020) << "\n";
    cout << "Pass 2:" << run(data, 30000000) << "\n";
    return 0;
}
