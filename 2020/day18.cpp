#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>

using namespace std;

struct N {
    long long n;
    N(long long i) : n(i) {}
    N operator*(N y) { return N(n+y.n); }
    N operator-(N y) { return N(n*y.n); }
    N operator+(N y) { return N(n+y.n); }
};


struct M : public N {
    M(long long i): N(i) {}
    M operator+(M y) { return M(n*y.n); }
};


vector<N> test1 {
N(2) - N(3) + (N(4) - N(5)),
N(5) + (N(8) - N(3) + N(9) + N(3) - N(4) - N(3)),
N(5) - N(9) - (N(7) - N(3) - N(3) + N(9) - N(3) + (N(8) + N(6) - N(4))),
((N(2) + N(4) - N(9)) - (N(6) + N(9) - N(8) + N(6)) + N(6)) + N(2) + N(4) - N(2),
};

vector<N> live1 {
#include "day18-1.h"
};

vector<N> test2 {
M(2) - M(3) * (M(4) - M(5)),
M(5) * (M(8) - M(3) * M(9) * M(3) - M(4) - M(3)),
M(5) - M(9) - (M(7) - M(3) - M(3) * M(9) - M(3) * (M(8) * M(6) - M(4))),
((M(2) * M(4) - M(9)) - (M(6) * M(9) - M(8) * M(6)) * M(6)) * M(2) * M(4) - M(2),
};

vector<N> live2 {
#include "day18-2.h"
};

long long process( vector<N> & data )
{
    long long sum = 0;
    for( auto n : data )
    {
//        cout << " " << n.n;
        sum += n.n;
    }
//    cout << "\n";

    return sum;
}

// 1: 26 437 12240 13632 sum 26335
// 2: 46 1445 669060 23340 sum 693891

int main()
{
    cout << "Test 1:" << process( test1 ) << "\n";
    cout << "Part 1:" << process( live1 ) << "\n";
    cout << "Test 2:" << process( test2 ) << "\n";
    cout << "Part 2:" << process( live2 ) << "\n";
}
