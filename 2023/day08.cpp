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
"RL\n"
"\n"
"AAA = (BBB, CCC)\n"
"BBB = (DDD, EEE)\n"
"CCC = (ZZZ, GGG)\n"
"DDD = (DDD, DDD)\n"
"EEE = (EEE, EEE)\n"
"GGG = (GGG, GGG)\n"
"ZZZ = (ZZZ, ZZZ)"
);

const string test1(
"LR\n"
"\n"
"11A = (11B, XXX)\n"
"11B = (XXX, 11Z)\n"
"11Z = (11B, XXX)\n"
"22A = (22B, XXX)\n"
"22B = (22C, 22C)\n"
"22C = (22Z, 22Z)\n"
"22Z = (22B, 22B)\n"
"XXX = (XXX, XXX)"
);

string directions = "";
map<string,tuple<string,string>> mapping;

void parse( const string & data )
{
    directions = "";
    mapping.clear();

    istringstream parse( data );
    string line;
    while( getline( parse, line ) )
    {
        if( line.empty() )
            continue;
        if( line.find('=') == string::npos )
            directions = line;
        else
        {
            string a = line.substr(0,3);
            string b = line.substr(7,3);
            string c = line.substr(12,3);
            mapping[a] = make_tuple(b,c);
        }
    }
}


int part1()
{
    string curr = "AAA";
    if( mapping.find(curr) == mapping.end() )
        return -1;

    int steps = 0;
    while( curr != "ZZZ" )
    {
        string left, right;
        tie(left,right) = mapping[curr];
        curr = directions[steps % directions.size()] == 'L' ? left : right;
        steps ++;
    }
    return steps;
}


int64_t lcm( int64_t a, int64_t b )
{
    return a * b / __gcd(a,b);
}


int64_t part2()
{
    int64_t result = 1;
    for( auto & k : mapping )
    {
        string g = k.first;
        if( g.back() != 'A' )
            continue;
        int steps = 0;
        while( g.back() != 'Z' )
        {
            string left, right;
            tie(left,right) = mapping[g];
            g = directions[steps % directions.size()] == 'L' ? left : right;
            steps ++;
        }
        result = lcm( result, steps );
    }

    return result;
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
        parse(test);
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day08.txt").rdbuf();
        parse(buffer.str());
    }

    cout << "Part 1: " << part1() << "\n";
    if( TEST )
        parse( test1 );
    cout << "Part 2: " << part2() << "\n";
}
