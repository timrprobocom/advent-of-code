#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

const string test(
"47|53\n"
"97|13\n"
"97|61\n"
"97|47\n"
"75|29\n"
"61|13\n"
"75|53\n"
"29|13\n"
"97|29\n"
"53|29\n"
"61|53\n"
"97|53\n"
"61|29\n"
"47|13\n"
"75|47\n"
"97|75\n"
"47|61\n"
"75|61\n"
"47|29\n"
"75|13\n"
"53|13\n"
"\n"
"75,47,61,53,29\n"
"97,61,53,29,13\n"
"75,29,13\n"
"75,97,47,61,53\n"
"61,13,29\n"
"97,13,75,29,47"
);

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;

StringVector split( string src, string delim )
{
    StringVector sv;
    for( int j = src.find(delim); j != -1; )
    {
        sv.push_back( src.substr(0,j) );
        src = src.substr(j+delim.size());
        j = src.find(delim);
    }
    sv.push_back(src);
    return sv;
}

map<int,set<int>> before;

bool compare( int & a, int & b )
{
    return before[a].find(b) == before[a].end();
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

    stringstream input;
    if( TEST )
    {
        input << test;
    }
    else 
    {
        input << ifstream("day05.txt").rdbuf();
    }

    vector<vector<int>> cases;

    string line;
    while( getline(input, line) )
    {
        if( line.empty() )
            continue;
        if( line[2] == '|')
        {
            int a = stoi(line.substr(0,2));
            int b = stoi(line.substr(3,2));
            before[b].insert(a);
        }
        else
        {
            cases.push_back( vector<int>() );
            for( auto & w : split(line,",") )
                cases.back().push_back(stoi(w));
                
        }
    }

    int sum1 = 0;
    int sum2 = 0;
    for( auto & casex : cases )
    {
        vector<int> order(casex);
        sort( order.begin(), order.end(), compare );
        if( order == casex )
            sum1 += casex[casex.size()/2];
        else
            sum2 += order[order.size()/2];
    }

    cout << "Part 1: " << sum1 << "\n";
    cout << "Part 2: " << sum2 << "\n";
}