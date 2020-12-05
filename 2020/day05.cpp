#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

//BFFFBBFRRR: row 70, column 7, seat ID 567.
//FFFBBBFRRR: row 14, column 7, seat ID 119.
//BBFFBBFRLL: row 102, column 4, seat ID 820.

/*
test = (
'BFFFBBFRRR',
'FFFBBBFRRR',
'BBFFBBFRLL'
)
*/


int main()
{
    ifstream fin("day05.txt");
    string line;
    vector<int> seats;
    while( getline( fin, line ) )
    {
        int seat = 0;
        for( char c : line )
        {
            seat <<= 1;
            if( c == 'B' || c == 'R' )
                ++seat;
        }
        seats.push_back( seat );
#ifdef DEBUG
        cout << line << " " << seat << "\n";
#endif
    }
    sort( seats.begin(), seats.end() );
    cout << "Part 1: " << seats.back() << "\n";
    int last = 0;
    for( int seat : seats )
    {
        if( last && seat != last+1 )
            break;
        last = seat;
    }
    cout << "Part 2: " << (last+1) << "\n";
}
