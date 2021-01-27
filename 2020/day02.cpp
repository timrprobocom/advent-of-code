#include <fstream>
#include <iostream>
#include <map>
#include <array>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

array<string,3> test = {
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc"
};

struct Problem {
    int d1;
    int d2;
    char ch;
    string str;

    friend istream& operator>> (istream & str, Problem & p )
    {
        string line;
        getline( str, line );
        if( line.empty() )
            return str;

        std::cout << "> " << line << "\n";
        int i1 = line.find('-');
        int i2 = line.find(' ');
        p.d1 = std::stoi( line.substr(0,i1) );
        p.d2 = std::stoi( line.substr(i1+1,i2-i1) );
        p.ch = line[i2+1];
        p.str = line.substr(i2+4);
        //std::cout << d1 << " " << d2 << " " << ch << " " << str << "\n";
        return str;
    }

    bool pass1()
    {
        int cnt = count( str.begin(), str.end(), ch );
        return (d1 <= cnt) && (cnt <= d2);
    }

    bool pass2()
    {
        return (str[d1-1] == ch) != (str[d2-1] == ch);
    }
};

int main()
{
    ifstream fin ( "day02.txt" );
    vector<Problem> live(
        istream_iterator<Problem>{fin},
        istream_iterator<Problem>{}
    );

    cout << "Pass 1: " 
        <<  count_if( live.begin(), live.end(), []( Problem & s ) { return s.pass1(); } )
        << "\n";
    cout << "Pass 2: " 
        <<  count_if( live.begin(), live.end(), []( Problem & s ) { return s.pass2(); } ) 
        << "\n";
}
