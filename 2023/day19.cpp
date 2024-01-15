#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;
typedef vector<vector<uint8_t>> ByteGrid;

const string test(
"px{a<2006:qkq,m>2090:A,rfg}\n"
"pv{a>1716:R,A}\n"
"lnx{m>1548:A,A}\n"
"rfg{s<537:gd,x>2440:R,A}\n"
"qs{s>3448:A,lnx}\n"
"qkq{x<1416:A,crn}\n"
"crn{x>2662:A,R}\n"
"in{s<1351:px,qqz}\n"
"qqz{s>2770:qs,m<1801:hdj,R}\n"
"gd{a>3333:R,R}\n"
"hdj{m>838:A,pv}\n"
"\n"
"{x=787,m=2655,a=1222,s=2876}\n"
"{x=1679,m=44,a=2067,s=496}\n"
"{x=2036,m=264,a=79,s=2244}\n"
"{x=2461,m=1339,a=466,s=291}\n"
"{x=2127,m=1623,a=2188,s=1013}"
);


typedef unsigned short Direction;

#define makedir(dx,dy) (((dx+1)<<4) | (dy+1))
#define getdx(dir)     ((dir>>4)-1)
#define getdy(dir)     ((dir&15)-1)

Direction U = makedir(0,-1);
Direction L = makedir(-1,0);
Direction D = makedir(0,1);
Direction R = makedir(1,0);

map<char,Direction> directions;

Direction backward( Direction d )
{
    int dx = getdx(d);
    int dy = getdy(d);
    return makedir(-dx,-dy);
}

void Initialize()
{
    directions['R'] = R;
    directions['L'] = L;
    directions['U'] = U;
    directions['D'] = D;
    directions['0'] = R;
    directions['1'] = D;
    directions['2'] = L;
    directions['3'] = U;
}

struct Step {
    char lhs;
    char comp;
    int rhs;
    string nxt;
};

typedef map<char,int> Part;

struct State {
    vector<Part> parts;
    map<string,vector<Step>> flows;
};

void parse( string & data, State & state )
{
    state.flows.clear();

    istringstream parse( data );
    string row;
    while( getline( parse, row ) )
    {
        if( row.empty() )
            continue;
        if( row[0] == '{' )
        {
            state.parts.resize(state.parts.size()+1);
            char xmas = '?';
            int val = 0;
            for( char c : row )
            {
                if( c == ',' || c == '}' )
                {
                    state.parts.back()[xmas] = val;
                    val = 0;
                }
                else if( isdigit(c) )
                    val = val * 10 + c - '0';
                else if( c != '=' )
                    xmas = c;
            }
        }
        else 
        {
            int i = row.find('{');
            string name = row.substr(0,i);
            string build;
            char lhs;
            char comp = '=';
            int val;
            for( char c : row.substr(i+1) )
            {
                if( c == '<' || c == '>' )
                {
                    lhs = build[0];
                    comp = c;
                    build.clear();
                }
                else if( c == ':' )
                {
                    val = stoi(build);
                    build.clear();
                }
                else if( c == ',' || c == '}' )
                {
                    state.flows[name].push_back(Step({lhs,comp,val,build}));
                    build.clear();
                    comp = '=';
                }
                else
                {
                    build += c;
                }
            }
        }
    }
}


void print( State & state )
{
    cout << "Flows:\n";
    for( auto & flow : state.flows )
    {
        cout << flow.first << ":\n";
        for( auto & step : flow.second )
        {
            if( step.comp == '=' )
                cout << "    " << step.nxt << "\n";
            else
                cout << "    " << step.lhs << step.comp << step.rhs << " --> " << step.nxt << "\n";
        }
    }
    cout << "parts:\n";
    for( auto & part : state.parts )
    {
        cout << "x=" << part['x'] 
            << " m=" << part['m']
            << " a=" << part['a']
            << " s=" << part['s'] << "\n";
    }

}


int64_t part1( State & state )
{
    int64_t sumx = 0;
    for( auto & part : state.parts )
    {
        string phase = "in";
        while( phase != "R" && phase != "A" )
        {
            for( auto & step : state.flows[phase] )
            {
                if( step.comp == '=' )
                {
                    phase = step.nxt;
                    break;
                }
                int val = part[step.lhs];
                if( (step.comp == '<' && val < step.rhs) 
                    || 
                    (step.comp == '>' && val > step.rhs)
                )
                {
                    phase = step.nxt;
                    break;
                }
            }
        }
        if( phase == "A" )
        {
            for( auto & p : part )
                sumx += p.second;
        }
    }
    return sumx;
}


struct Range
{
    int lo;
    int hi;
};

typedef map<char,Range> PartRange;

PartRange copy( PartRange & pr )
{
    PartRange part;
    for( auto k : pr )
        part[k.first] = Range({k.second.lo,k.second.hi});
    return part;
}

int64_t part2( State & state )
{
    PartRange part;
    part['x'] = Range({1,4000});
    part['m'] = Range({1,4000});
    part['a'] = Range({1,4000});
    part['s'] = Range({1,4000});

    deque<tuple<string,PartRange>> pending;
    pending.push_back( make_tuple("in",part) );
    int64_t sumx = 0;

    while( !pending.empty() )
    {
        auto [phase, part] = pending.front();
        pending.pop_front();

        if( phase == "A" )
        {
            int64_t prod = 1;
            for( auto & p : part )
                prod *= p.second.hi - p.second.lo + 1;
            sumx += prod;
            continue;
        }
        if( phase == "R" )
            continue;
        for( auto & step : state.flows[phase] )
        {
            if( step.comp == '=' )
            {
                pending.push_back( make_tuple(step.nxt,part) );
                break;
            }

            // I originally had code to check for the condition where the
            // "need" value was completely above or below the range, but
            // it turns out that never happens.  EVERY rule splits a range.

            if( step.comp == '<' )
            {
                //  x < 400   0,399   all take the jump
                //  x < 400   200,600 200..399 take the jump 400-600 move on
                //  x < 400   500,600 all move on
                PartRange p1 = copy(part);
                p1[step.lhs].hi = step.rhs-1;
                pending.push_back(make_tuple(step.nxt,p1));
                part[step.lhs].lo = step.rhs;
            }
            else
            {
                //  x > 400   0,400   all move on
                //  x > 400   200,600 200..400 move on 401-600 take the jump
                //  x > 400   500,600 all take the jump
                PartRange p1 = copy(part);
                p1[step.lhs].lo = step.rhs+1;
                pending.push_back(make_tuple(step.nxt,p1));
                part[step.lhs].hi = step.rhs;
            }
        }
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

    string data;
    if( TEST )
    {
        data = test;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day19.txt").rdbuf();
        data = buffer.str();
    }

    // Parses into the globals parts and flows.

    State state;
    parse(data,state);
    if( DEBUG )
        print(state);

    cout << "Part 1: " << part1(state) << "\n";
    cout << "Part 2: " << part2(state) << "\n";
}
