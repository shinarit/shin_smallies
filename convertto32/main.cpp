#include <iostream>
#include <fstream>

#include "SDL/SDL.h"

int main(int argc, char* argv[])
{
  if (argc != 3)
  {
    std::cerr << "usage: " << argv[0] << " <source bmp> <target bmp>\n";
    return 1;
  }
  SDL_Init( SDL_INIT_EVERYTHING );

  SDL_Surface* source;
  if (0 == (source = SDL_LoadBMP(argv[1])))
  {
    std::cerr << "error while opening " << argv[1] << '\n';
    return 2;
  }
  
  if (4 == source->format->BytesPerPixel)
  {
    std::cout << "bmp already 32 bit\n";
    SDL_SaveBMP(source, argv[2]);
  }
  else
  {
    SDL_PixelFormat format;
    format.palette = 0;          //palette
    format.BitsPerPixel = 32;    //bpp
    format.BytesPerPixel = 4;    //Bpp
    format.Rmask = 0x00ff0000; //rmask
    format.Gmask = 0x0000ff00; //gmask
    format.Bmask = 0x000000ff; //bmask

    SDL_Surface* target;
    if (0 == (target = SDL_ConvertSurface(source, &format, 0)))
    {
      std::cerr << "error while converting\n";
      return 3;
    }
    
    if (-1 == SDL_SaveBMP(target, argv[2]))
    {
      std::cerr << "error while saving to " << argv[2] << '\n';
      return 4;
    }
    SDL_FreeSurface( target );
  }

  SDL_FreeSurface( source );

  SDL_Quit();
  return 0;  
}
