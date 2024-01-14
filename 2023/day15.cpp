#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <deque>
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
"rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
);


int dohash( string & s )
{
    int sum = 0;
    for( char c : s )
        sum = ((sum + c) * 17) % 256;
    return sum;
}


int part1( string & data )
{
    int sum = 0;
    string s;
    istringstream parse(data);
    while( getline(parse, s, ',') )
        sum += dohash(s);
    return sum;
}


int part2( string & data )
{
    typedef tuple<string,int> myPair;
    vector<vector<myPair>> boxes(256);

    string part;
    istringstream parse(data);
    while( getline( parse, part, ',' ) )
    {
        if( part.back() == '-' )
        {
            part.resize(part.size()-1);
            auto & box = boxes[dohash(part)];
            auto b = find_if( box.begin(), box.end(), [part](myPair & b){
                return get<0>(b) == part;
            });
            if( b != box.end() )
                box.erase(b);
        }
        else
        {
            int i = part.find('=');
            int val = stoi(part.substr(i+1));
            part.resize(i);

            auto & box = boxes[dohash(part)];
            auto b = find_if( box.begin(), box.end(), [part](myPair & b){
                return get<0>(b) == part;
            });
            if( b != box.end() )
                *b = make_tuple(part,val);
            else
                box.push_back( make_tuple(part,val) );
        }
    }
    int sum = 0;
    for( int i = 0; i < boxes.size(); i++ )
        for( int j = 0; j < boxes[i].size(); j++ )
            sum += (i+1) * (j+1) * get<1>(boxes[i][j]);
    return sum;
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

    string data;
    if( TEST )
    {
        data = test;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day15.txt").rdbuf();
        data = buffer.str();
    }

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}


