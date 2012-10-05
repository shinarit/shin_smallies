#include <iostream>
#include <fstream>

#include "SDL/SDL.h"

int main(int argc, char* argv[])
{
  std::ofstream ctt("CON");
  freopen( "CON", "w", stdout );
  freopen( "CON", "w", stderr );
  if (argc != 3)
  {
    std::cout << "usage: " << argv[0] << " <source bmp> <target bmp>\n";
    ctt.close();
    return 1;
  }
  SDL_Init( SDL_INIT_EVERYTHING );

  SDL_Surface* pic(SDL_LoadBMP(argv[1]));

  SDL_FreeSurface( pic );

  SDL_Quit();
  
}
