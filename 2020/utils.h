#pragma once

struct Point {
    int x;
    int y;
    Point( int _x=0, int _y=0 )
        : x(_x)
        , y(_y)
        {}

    bool operator< (const Point & other) const
    {
        return x < other.x || y < other.y;
    }

    bool operator== (const Point & other) const
    {
        return x==other.x && y==other.y;
    }

    bool operator!= (const Point & other) const
    {
        return x!=other.x || y!=other.y;
    }

    Point operator+( const Point & other )
    {
        return Point( x+other.x, y+other.y );
    }

    Point& operator+=( const Point & other )
    {
        x += other.x;
        y += other.y;
        return *this;
    }

    Point operator*( const int factor )
    {
        return Point( x*factor, y*factor );
    }

    Point& operator*=( const int factor )
    {
        x *= factor;
        y *= factor;
        return *this;
    }

    int mandist()
    {
        return abs(x) + abs(y);
    }

    void left()
    {
        int x = self.x
        self.x = self.y
        self.y = -x;
    }

    void right()
    {
        int x = self.x
        self.x = -self.y
        self.y = x;
    }
};
