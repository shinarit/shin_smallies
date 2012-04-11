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

const Color black(0, 0, 0);

//simple class containing the x, y coordinates
struct Coordinate
{
  Coordinate(int x = 0, int y = 0): x(x), y(y)
  {}
  int x;
  int y;
};

//use the same struct as size
typedef Coordinate Size;
typedef Coordinate Speed;

void DrawCircle(Coordinate center, int size, Color col, bool fill = false);
void DrawLine(Coordinate begin, Coordinate end, Color col);
void DrawShape(Coordinate* begin, Coordinate* end, Color color, bool fill = false);

Size GetSize();

//
// interface for the actual logic's functions
//

void Init();
void DrawFrame();
void Exit();

#endif

