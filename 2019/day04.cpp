#include <iostream>
#include <algorithm>
#include <array>

int tests[6] = { 111111, 223450, 123789, 112233, 123444, 111122 };

//ranges = (254032,789860+1)

int valid( int pw, int part )
{
    int dig[6];
    for( int i = 0; i < 6; i++ )
    {
        dig[5-i] = pw % 10;
        pw /= 10;
    }

    std::array<int,10> cnts = { 0 };

    for( int i = 0; i < 6; i++ )
    {
        if( i < 5 && dig[i] > dig[i+1] )
            return 0;
        cnts[dig[i]]++;
    }

    return std::any_of( cnts.begin(), cnts.end(), 
        part == 1 
            ? [](int i){return i>=2;}
            : [](int i){return i==2;}
    );
}


int main()
{
    for( auto t : tests )
    {
        std::cout << t << " P1: " << valid(t,1) << " P2: " << valid(t,2) << "\n";
    }
    
    int cnt1 = 0;
    int cnt2 = 0;
    for( int t = 254032; t <= 789860; t++ )
    {
        cnt1 += valid( t, 1 );
        cnt2 += valid( t, 2 );
    }

    std::cout << "Part 1 : " << cnt1 << "\n"
              << "Part 2 : " << cnt2 << "\n";
}
