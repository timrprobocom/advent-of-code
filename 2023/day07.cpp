#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;

const string test(
"32T3K 765\n"
"T55J5 684\n"
"KK677 28\n"
"KTJJT 220\n"
"QQQJA 483"
);

string order = "23456789TJQKA";

/*
#6 Five of a kind, where all five cards have the same label: AAAAA
#5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
#4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
#3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
#2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
#1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
#0 High card, where all cards' labels are distinct: 23456
*/

map<char,int> Counter(string s)
{
    map<char,int> cts;
    for( char c : s )
        cts[c] += 1;
    return cts;
}

int grade( string hand )
{
    int value = 0;
    for( char c : hand )
        value = value * 15 + order.find(c);

    map<char,int> cts = Counter(hand);

    // For pass 2, replace the joker by the most common card.

    if( order[0] == 'J' && hand.find('J') != string::npos )
    {
        char pick = 'J';
        for( int chk = 5; pick == 'J' && chk > 0; chk-- )
        {
            for( auto & p : cts )
            {
                if( p.second == chk && p.first != 'J' )
                {
                    pick = p.first;
                    break;
                }
            }
        }

        if( pick != 'J' )
        {
            int i;
            while( (i = hand.find('J')) != string::npos )
                hand[i] = pick;

            cts = Counter(hand);
        }
    }

    vector<int> vals;
    for( auto & p : cts )
        vals.push_back(p.second);

    sort( vals.begin(), vals.end(), [](int a, int b){return a>b;} );

    if( vals.size() == 1 )
        return value + 6000000;
    if( vals.size() == 2 )
    {
        if( vals[0] == 4 )
            return value + 5000000;
        else
            return value + 4000000;
    }
    if( vals.size() == 3 )
    {
        if( vals[0] == 3 )
            return value + 3000000;
        else
            return value + 2000000;
    }
    if( vals.size() == 4 )
        return value + 1000000;
    return value;
}

struct Hand {
    int score;
    string hand;
    int bid;
};

int part1(string & data )
{
    string word;
    string hand;
    vector<Hand> hands;
    istringstream parse(data);
    while( parse >> word )
    {
        if( word.size() == 5 )
        {
            hand = word;
        }
        else
        {
            hands.push_back( 
                Hand({grade(hand), hand, stoi(word)})
            );
        }
    }

   sort( hands.begin(), hands.end(), [](Hand & a, Hand & b){ return a.score < b.score; });
   if( DEBUG )
   {
       for( int i = 0; i < hands.size(); i++ )
           cout << (i+1) << " " << hands[i].score << " " << hands[i].hand << " " << ((i+1)*hands[i].bid) << "\n";
   }
   int sumx = 0;
   for( int i = 0; i < hands.size(); i++ )
       sumx += (i+1) * hands[i].bid;
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
        buffer << ifstream("day07.txt").rdbuf();
        data = buffer.str();
    }

    cout << "Part 1: " << part1(data) << "\n";
    order = "J23456789TQKA";
    cout << "Part 2: " << part1(data) << "\n";
}
