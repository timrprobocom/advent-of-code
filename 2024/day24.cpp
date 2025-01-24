#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <limits.h>
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
"x00: 1\n"
"x01: 0\n"
"x02: 1\n"
"x03: 1\n"
"x04: 0\n"
"y00: 1\n"
"y01: 1\n"
"y02: 1\n"
"y03: 1\n"
"y04: 1\n"
"\n"
"ntg XOR fgs -> mjb\n"
"y02 OR x01 -> tnw\n"
"kwq OR kpj -> z05\n"
"x00 OR x03 -> fst\n"
"tgd XOR rvg -> z01\n"
"vdt OR tnw -> bfw\n"
"bfw AND frj -> z10\n"
"ffh OR nrd -> bqk\n"
"y00 AND y03 -> djm\n"
"y03 OR y00 -> psh\n"
"bqk OR frj -> z08\n"
"tnw OR fst -> frj\n"
"gnj AND tgd -> z11\n"
"bfw XOR mjb -> z00\n"
"x03 OR x00 -> vdt\n"
"gnj AND wpb -> z02\n"
"x04 AND y00 -> kjc\n"
"djm OR pbm -> qhw\n"
"nrd AND vdt -> hwm\n"
"kjc AND fst -> rvg\n"
"y04 OR y02 -> fgs\n"
"y01 AND x02 -> pbm\n"
"ntg OR kjc -> kwq\n"
"psh XOR fgs -> tgd\n"
"qhw XOR tgd -> z09\n"
"pbm OR djm -> kpj\n"
"x03 XOR y03 -> ffh\n"
"x00 XOR y04 -> ntg\n"
"bfw OR bqk -> z06\n"
"nrd XOR fgs -> wpb\n"
"frj XOR qhw -> z04\n"
"bqk OR frj -> z07\n"
"y03 OR x01 -> nrd\n"
"hwm AND bqk -> z03\n"
"tgd XOR rvg -> z12\n"
"tnw OR pbm -> gnj"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day24"

typedef map<string,short> gates_t;
typedef vector<StringVector> rules_t;

short operate(gates_t & gates, string a, string op, string b)
{
    if( op == "AND" )
        return gates[a] & gates[b];
    if( op == "OR" )
        return gates[a] | gates[b];
    if( op == "XOR" )
        return gates[a] ^ gates[b];

    return 0;
}

int64_t binary( gates_t & gates, char c )
{
    int64_t sumx = 0;
    for( auto & kv : gates )
    {
        if( kv.first[0] == c )
        {
            int n = stoi(kv.first.substr(1));
            sumx |= (int64_t)kv.second << n;
        }
    }
    return sumx;
}

string printrow( StringVector & sv, char sep=' ' )
{
    string s;
    for( auto & psv : sv )
    {
        if( !s.empty() )
            s += sep;
        s += psv;
    }
    return s;
}


int64_t do_a_run(gates_t & gates, rules_t & incodes, map<string,string> & swap)
{
    gates_t xgates;
    for( auto & kv : gates )
        if( kv.first[0] == 'x' || kv.first[0] == 'y' )
            xgates[kv.first] = kv.second;
    
    rules_t codes( incodes.begin(), incodes.end() );
    while( !codes.empty() )
    {
        rules_t undone;
        for( auto & row : codes )
        {
            string a = row[0];
            string op = row[1];
            string b = row[2];
            string r = row[4];

            if( is_in(a, xgates) && is_in(b, xgates) )
            {
                if( is_in( r, swap ) )
                    r = swap[r];
                xgates[r] = operate(xgates, a, op, b);
            } 
            else
                undone.push_back( row );
        }
        if( undone.size() == codes.size() )
            return -1;

        codes.swap( undone );
    }
    return binary(xgates,'z');
}


// Parse the rules.

// Xn XOR Yn => Mn
// Xn AND Yn => Nn
// Cn-1 AND Mn => Rn
// Cn-1 XOR Mn -> Zn
// Rn OR Nn -> Cn


StringVector swaps;

int64_t part1( gates_t & gates, rules_t & incodes )
{
    set<string> zs;
    for( auto & pv : incodes )
        if( pv[4][0] == 'z' )
            zs.insert( pv[4] );

    // Make our expectations.

    string lastcarry( "xxx" );
    gates_t outgates;
    gates_t xgates;
    rules_t codes( incodes.begin(), incodes.end() );
    for( auto rzv : zs )
    {
        string x = string("x") + rzv.substr(1);
        string y = string("y") + rzv.substr(1);

        set<string> sources( {x, y} );
        xgates[x] = gates[x];
        xgates[y] = gates[y];
        vector<StringVector> new_rules( 5, { "   ","   ","   ","  ","   " } );
        while( !codes.empty() )
        {
            rules_t undone;
            for( auto & rule : codes )
            {
                string c1 = rule[0];
                string op = rule[1];
                string c2 = rule[2];
                string r = rule[4];
                if( is_in( c1, xgates) && is_in( c2, xgates ) )
                {
                    if( op == "AND" )
                    {
                        xgates[r] = xgates[c1] & xgates[c2];
                        if( is_in(c1, sources) && is_in(c2, sources) )
                            new_rules[3] = rule;
                        else
                            new_rules[2] = rule;
                    }
                    else if( op == "OR" )
                    {
                        xgates[r] = xgates[c1] | xgates[c2];
                        new_rules[4] = rule;
                    }
                    else if( op == "XOR" )
                    {
                        xgates[r] = xgates[c1] ^ xgates[c2];
                        if( is_in(c1, sources) && is_in(c2, sources) )
                            new_rules[0] = rule;
                        else
                            new_rules[1] = rule;
                    }
                }
                else
                    undone.push_back( rule );
            }
            if( undone.size() == codes.size() )
                break;
            codes.swap( undone );
        }

        // Capture the output.

        outgates[rzv] = xgates[rzv];
        if( DEBUG )
        {
            for( auto & row : new_rules )
                cout << printrow(row) << "   ";
            cout << endl;
        }

        // Validate the rules to find the bugs.

        if( new_rules[1][0] != "   " )
        {
            if( new_rules[1][4][0] != 'z' )
            {
                if( DEBUG )
                    cout << "WRONG " << printrow(new_rules[1]) << " swap " <<  rzv << " and " << new_rules[1][4] << "\n";
                swaps.push_back( rzv );
                swaps.push_back( new_rules[1][4] );
            }
            if( !is_in( new_rules[0][4], new_rules[1] ) )
            {
                string shd = "???";
                if( new_rules[1][0] == lastcarry )
                    shd = new_rules[1][2];
                else
                    shd = new_rules[1][0];
                if( DEBUG )
                    cout << "WRONG " << new_rules[0][4] << " not present in " << printrow(new_rules[1]) << " swap " << new_rules[0][4] << " " << shd << "\n";
                swaps.push_back( new_rules[0][4] );
                swaps.push_back( shd );
            }
        }
        if( new_rules[4][4] != "   " )
            lastcarry = new_rules[4][4];
    }
    return binary(outgates,'z');
}

// This just validates the swaps.

int64_t validate( gates_t & gates, rules_t & codes )
{
    int64_t xx = binary(gates, 'x');
    int64_t yy = binary(gates, 'y');
    int64_t target = xx+yy;

    map<string,string> swapmap;
    for( int i = 0; i < swaps.size(); i += 2 )
    {
        swapmap[swaps[i]] = swaps[i+1];
        swapmap[swaps[i+1]] = swaps[i];
    }
    cout << gates.size() << " " << codes.size() << " " << swapmap.size() << "\n";
    int64_t ans = do_a_run(gates, codes, swapmap);
    if( DEBUG )
        cout << target << " ==? " << ans << "\n";
    return target == ans;
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

    string input = TEST ? test : file_contents(DAY".txt");

    map<string,short> gates;
    vector<vector<string>> codes;
    for( auto & line : split(input) )
    {
        if( line.empty() )
            continue;
        if( line[3] == ':' )
            gates[line.substr(0,3)] = line[5]-'0';
        else
            codes.push_back( split(line, " ") );
    }

    cout << "Part 1: " << part1(gates, codes) << "\n";
    if( DEBUG && !TEST )
        cout << "Validate: " << validate(gates, codes) << "\n";
    sort(swaps.begin(), swaps.end());
    cout << "Part 2: " << printrow(swaps,',') << "\n";
}
