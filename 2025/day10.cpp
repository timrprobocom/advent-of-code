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

#include "utils.h"

using namespace std;

const string test(
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n"
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n"
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
);

#define DAY "day10"

bool DEBUG = false;
bool TEST = false;
bool TIMING = false;

struct Unit {
    string      lights;
    IntMatrix   presses;
    IntVector   joltages;
};

#define _in_
#define _out_

void parse(
    _in_  StringVector & data,
    _out_ vector<Unit> & units
)
{
    units.resize( data.size() );
    auto unit = units.begin();

    for( auto & line : data )
    {
        auto parts = split(line, " ");

        auto pf = parts.front();
        unit->lights = pf.substr(1, pf.size()-2);

        auto pb = parts.back().substr(1, parts.back().size()-2);
        unit->joltages = split_int(pb, ",");

        for( int i = 1; i < parts.size()-1; i++ )
        {
            auto pb = parts[i].substr(1, parts[i].size()-2);
            unit->presses.push_back( split_int(pb, ",") );
        }

        unit++;
    }
}


string toggle(string lights, const IntVector & switches) 
{
    for( auto i : switches )
    {
        if( lights[i] == '#' )
            lights[i] = '.';
        else
            lights[i] = '#';
    }
    return lights;
}

int64_t part1 ( vector<Unit> & units )
{
    int sum = 0;
    for( auto & unit : units )
    {
        string target = unit.lights;
        IntMatrix & prs = unit.presses;
        int found = 0;
        int bits = prs.size();

        deque<tuple<int,int>> queue;
        for( int j = 0; j < bits; j++ )
            queue.push_back( make_tuple(1<<j,1) );

        while( !queue.empty() )
        {
            auto [curr, count] = queue.front();
            queue.pop_front();

            // Try this combination.

            string mylights(target.size(), '.');
            for( int j = 0; j < bits; j++ )
                if( curr & (1<<j) )
                    mylights = toggle( mylights, prs[j] );

            if( mylights == target )
            {
                sum += count;
                break;
            }

            for( int j = 0; j < prs.size(); j++ )
                if( (1 << j) > curr )
                    queue.push_back( make_tuple(curr | (1 << j), count+1) );
		}
	}
	return sum;
}

double EPSILON = 1e-9;

struct Matrix {
    vector<vector<double>>   data;
    int         m_rows;
    int         m_cols;
    vector<int> dependents;
    vector<int> independents;

    Matrix( Unit & unit )
        : m_rows (unit.joltages.size())
        , m_cols (unit.presses.size())
    {
        data.resize( m_rows );
        for( auto & d : data )
            d.resize( m_cols+1 );

        // Add all of our buttons.

        for( int c = 0; c < unit.presses.size(); c++ )
            for( auto p : unit.presses[c] )
                data[p][c] = 1.0;
    
        // Add the joltages in the last column.

        for( int r = 0; r < unit.joltages.size(); r++ )
            data[r][m_cols] = unit.joltages[r];
    }

    void print()
    {
        cout << "[\n";
        for( auto & row : data )
        {
            cout << "  [";
            for( auto col : row )
                cout << " " << col;
            cout << " ]\n";
        }
        cout << "]\n";
        cout << " " << m_rows << " rows " << m_cols << " cols\n";
        cout << "i [";
        for( auto c : independents )
            cout << " " << c;
        cout << " ] d [";
        for( auto c : dependents )
            cout << " " << c;
        cout << " ]\n";
    }

    // https://en.wikipedia.org/wiki/Gaussian_elimination
    void gaussian_elimination() 
    {
        int pivot = 0;
        int col = 0;

        while( pivot < m_rows && col < m_cols )
        {
            // Find the best pivot row for this column.
            // (I think this is the row that contains the largest absolute value.)

            auto m = max_element( data.begin()+pivot, data.end(), 
                [col](vector<double> & a, vector<double> & b) { return abs(a[col]) < abs(b[col]); });
            double maxv = abs((*m)[col]);
            int maxrow = m - data.begin();

            if (DEBUG )
                cout << "DFS, pivot " << pivot << " col " << col << " max is " << maxrow << " " << maxv << "\n";

            // If the best value is zero, this is a free variable.
            if( maxv < EPSILON )
            {
                independents.push_back( col );
                col++;
                continue;
            }

            // Swap m_rows and mark this column as dependent.
            data[pivot].swap( data[maxrow] );
            dependents.push_back( col );

            // Normalize pivot row.  Being triangular, there are only values from col on.
            auto pivot_value = data[pivot][col];
            for( int c = col; c <= m_cols; c++ )
                data[pivot][c] /= pivot_value;
            if( DEBUG )
                cout << "pivot value " << pivot_value << "\n";

            // Eliminate this column in all other rows.
            for( int r = 0; r < m_rows; r++ )
            {
                if( r != pivot )
                {
                    auto factor = data[r][col];
                    if( abs(factor) > EPSILON )
                    {
                        for( int c = col; c <= m_cols; c++ )
                        {
                            data[r][c] = (data[r][c] - factor * data[pivot][c]);
                        }
                    }
                }
            }

            pivot++;
            col++;
        }

        // Any remaining columns are free variables.
        for( int c = col; c < m_cols; c++ )
            independents.push_back( c );
    }

    // Check if the given values for our independent variables are valid. If so, return the total button presses.

    int valid( vector<int> & values )
    {
        // We start with how many times we've pressed the free variables.
        auto total = accumulate(values.begin(), values.end(), 0 );

        // Calculate dependent variable values based on independent variables.
        for( int row = 0; row < dependents.size(); row++ )
        {
            auto val = data[row][m_cols];
            for( int i = 0; i < independents.size(); i++ )
                val -= data[row][independents[i]] * double(values[i]);

            // We need non-negative, whole numbers for a valid solution.
            if( val < -EPSILON )
                return -1;
            int rounded = round(val);
            if( abs(val-rounded) > EPSILON )
                return -1;

            total += rounded;
        }

        return total;
    }
};

int dfs(Matrix & mat, int idx, vector<int> & values, int  min , int max)
{
    int total = 0;

    // When we've assigned all independent variables, check if it's a valid solution.
    if( idx == mat.independents.size() )
    {
        total = mat.valid(values);
        if( total >= 0 && total < min )
            min = total;
        return min;
    }

    // Try different values for the current independent variable.
    total = accumulate(values.begin(), values.begin()+idx, 0);
    for( int val = 0; val < max; val++ )
    {
        // Optimization: If we ever go above our min, we can't possibly do better.
        if( total+val >= min )
            break;
        values[idx] = val;
        min = dfs(mat, idx+1, values, min, max);
    }
    return min;
}

int solve( Unit & unit )
{
    Matrix matrix( unit );
    if( DEBUG )
    {
        cout << "BEFORE\n";
        matrix.print();
    }
    matrix.gaussian_elimination();
    if( DEBUG)
    {
        cout << "AFTER\n";
        matrix.print();
    }

    // Now we can DFS over a much smaller solution space.

    int max = *max_element( unit.joltages.begin(), unit.joltages.end() ) + 1;
    int min = 999999999;

    vector<int> values( matrix.independents.size() );
    return dfs(matrix, 0, values, min, max);
}


int64_t part2 ( vector<Unit> & units )
{
    return accumulate( 
        units.begin(), units.end(), 0, 
        [](int sum, Unit & unit) { return sum + solve(unit); } 
    );
}

int main( int argc, char ** argv )
{
    string name = *argv;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    string input = TEST ? test : file_contents(DAY".txt");
    StringVector lines = split(input);

    vector<Unit> units;
    parse( lines, units );
    
    cout << "Part 1: " << part1(units) << "\n";
    cout << "Part 2: " << part2(units) << "\n";
}
