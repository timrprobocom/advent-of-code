#pragma once

struct Point {
    int x;
    int y;
    int z;
    Point( int _x=0, int _y=0, int _z=0 )
        : x(_x)
        , y(_y)
        , z(_z)
        {}

    bool operator< (const Point & other) const
    {
        return x < other.x || 
            ((x == other.x) && (y < other.y)) ||
            (x == other.x) && (y == other.y) && (z < other.z);
    }

    bool operator== (const Point & other) const
    {
        return x==other.x && y==other.y && z==other.z;
    }

    bool operator!= (const Point & other) const
    {
        return x!=other.x || y!=other.y || z!=other.z;
    }

    Point operator+( const Point & other )
    {
        return Point( x+other.x, y+other.y, z+other.z );
    }

    Point operator-( const Point & other ) const
    {
        return Point( x-other.x, y-other.y, z-other.z );
    }

    Point& operator+=( const Point & other )
    {
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
    }

    int mandist()
    {
        return abs(x) + abs(y) + abs(z);
    }

    int mandist( const Point & other) const
    {
        return (*this-other).mandist();
    }

    void left()
    {
        int tmp = x;
        x = y;
        y = -tmp;
    }

    // This is the same as rotatez.
    void right()
    {
        int tmp = x;
        x = -y;
        y = tmp;
    }

    Point rotatex() const
    {
        return Point(x,z,-y);
    }

    Point rotatey() const
    {
        return Point(z,y,-x);
    }

    Point rotatez() const
    {
        return Point(-y,x,z);
    }

    void rotate(char axis)
    {
        Point copy(*this);
        if( axis == 'x' )
        {
            y = copy.z;
            z = -copy.y;
        }
        else if( axis == 'y' )
        {
            x = copy.z;
            z = -copy.x;
        }
        else if( axis == 'z' )
        {
            x = -copy.y;
            y = copy.x;
        }
    }
};

