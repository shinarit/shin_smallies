#ifndef WIZ_DRAW_H_
#define WIZ_DRAW_H_

const int FramePerSecond = 25;

//
// interface file for drawing layer functions
//

typedef unsigned char uchar;

//simple RGB structure, [0 - 255] range
struct Color
{
  Color(uchar red, uchar green, uchar blue): red(red), green(green), blue(blue)
  {}
  uchar red;
  uchar green;
  uchar blue;
};

namespace Colors
{
  const Color black(0, 0, 0);
  const Color white(255, 255, 255);
  const Color red(255, 0, 0);
  const Color green(0, 255, 0);
  const Color blue(0, 0, 255);
}

//simple class containing the x, y coordinates
struct Coordinate
{
  typedef double CoordType;
  Coordinate(CoordType x = CoordType(), CoordType y = CoordType()): x(x), y(y)
  {}
  CoordType x;
  CoordType y;

  Coordinate& operator+=(const Coordinate& rhs);
};

Coordinate operator-(const Coordinate& op);
Coordinate operator+(const Coordinate& lhs, const Coordinate& rhs);
Coordinate operator-(const Coordinate& lhs, const Coordinate& rhs);
Coordinate operator*(const Coordinate& lhs, const Coordinate::CoordType rhs);
Coordinate operator/(const Coordinate& lhs, const Coordinate::CoordType rhs);

Coordinate::CoordType Length(const Coordinate& vektor);
Coordinate::CoordType Distance(const Coordinate& lhs, const Coordinate& rhs);

typedef Coordinate Size;

void DrawCircle(Coordinate center, int size, Color col, bool fill = false);
void DrawLine(Coordinate begin, Coordinate end, Color col);
void DrawShape(Coordinate* begin, Coordinate* end, Color color, bool fill = false);

Size GetSize();

//
// interface for the actual logic's functions
//
#endif

