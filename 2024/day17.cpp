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

using namespace std;

const char * test[3] = {
"Register A: 729\n"
"Register B: 0\n"
"Register C: 0\n"
"\n"
"Program: 0,1,5,4,3,0",

"Register A: 2024\n"
"Register B: 0\n"
"Register C: 0\n"
"\n"
"Program: 0,1,5,4,3,0",

"Register A: 117440\n"
"Register B: 0\n"
"Register C: 0\n"
"\n"
"Program: 0,3,5,4,3,0"
};

const string live(
"Register A: 63687530\n"
"Register B: 0\n"
"Register C: 0\n"
"\n"
"Program: 2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0"
);

bool DEBUG = false;
bool TEST = false;

const char * opcodes[] = {
//    0      1      2      3      4      5      6      7
    "adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"
};

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

struct CPU {
    uint64_t A;
    uint64_t B;
    uint64_t C;
    short P;
    vector<short> program;

    CPU( const string & data )
        : P ( 0 )
    {
        for( auto line : split(data, "\n") )
        {
            if( !line.empty() )
            {
                StringVector words = split(line, " ");
                if( words[0] == "Register" )
                {
                    int val = stoi(words[2]);
                    switch( words[1][0] )
                    {
                        case 'A':
                            A = val;
                            break;
                        case 'B':
                            B = val;
                            break;
                        case 'C':
                            C = val;
                            break;
                    }
                }
                else if( words[0] == "Program:" )
                {
                    for( char c : words[1] )
                        if( c != ',' )
                            program.push_back( c-'0' );
                }
            }
        }
    }

    int execute( short opc, short opd )
    {
        switch( opc )
        {
            case 0: // adv
                A = A >> combo(opd);
                break;
            case 6: // bdv
                B = A >> combo(opd);
                break;
            case 7: // cdv
                C = A >> combo(opd);
                break;
            case 1: // bxl
                B = B ^ opd;
                break;
            case 2: // bst
                B = combo(opd) & 7;
                break;
            case 3: // jnz
                if( A )
                    P = opd - 2;
                break;
            case 4: // bxc
                B = B ^ C;
                break;
            case 5: // out
                return combo(opd) & 7;
        }
        return -1;
    }

    vector<short> run()
    {
        vector<short> result;
        while( P < program.size() )
        {
            short i = program[P];
            short j = program[P+1];
            if( DEBUG )
            {
                cout << P << ": " 
                     << i << " " << opcodes[i] << "   " << j << "->" << combo(j)
                     << " A=" << A << " B=" << B << " C=" << C << "\n";
            }
            short k = execute(i, j);
            if( k >= 0 )
                result.push_back(k);
            P += 2;
        }
        return result;
    }

    int64_t combo(int n)
    {
        switch( n )
        {
            case 0:
            case 1:
            case 2:
            case 3:
                return n;
            case 4:
                return A;
            case 5:
                return B;
            case 6:
                return C;
        }
        return -1;
    }
};

string part1( const string & program )
{
    CPU cpu(program);
    vector<short> result = cpu.run();
    string ret;
    for( auto v : result )
    {
        if( !ret.empty() )
            ret += ",";
        ret += '0'+v;
    }
    return ret;
}

short step( uint64_t A, vector<short> & v )
{
    uint64_t  B = (A & 7) ^ v[0];
    return B ^ (A >> B) ^ v[1];
}

uint64_t part2( const string & program)
{
    CPU cpu(program);

    // The two variables here are the operands to the bxl statements.

    vector<short> consts;
    for( int i = 0; i < cpu.program.size(); i+=2 )
    {
        if( cpu.program[i] == 1 )
            consts.push_back( cpu.program[i+1] );
    }

    // We start from the program, backwards, and find the values that create 
    // create the instruction for that step.  There might be several.

    vector<uint64_t> queue{ 0,1,2,3,4,5,6,7 };
    vector<uint64_t> possible;
    for( int i = cpu.program.size()-1; i >= 0; i-- )
    {
        short match = cpu.program[i];

        // Run the program sequence for each potential A value.  Save the ones
        // that produce the desired value.

        possible.clear();
        copy_if( 
            queue.begin(),
            queue.end(),
            back_inserter(possible), 
            [&consts, match](uint64_t in){return (step(in,consts)&7)==match;}
        );

        // Now produce the possible A values for the next digit.
        
        queue.clear();
        for( auto p : possible )
            for( int i = 0; i < 8; i++ )
                queue.push_back( p*8+i );
    }

    // Verify.
    uint64_t mn = *min_element( possible.begin(), possible.end() );
    cpu.A = mn;
    if( cpu.program != cpu.run() )
        cout << "MISMATCH ";

    return mn;
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

    if( TEST )
    {
        for( auto & s : test )
            cout << "Part 1: " << part1(s) << "\n";
    }
    else
    {
        cout << "Part 1: " << part1(live) << "\n";
        cout << "Part 2: " << part2(live) << "\n";
    }
}
