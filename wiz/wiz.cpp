#include "wiz.hpp"
#include "drawinterface.hpp"
#include "flyerz.hpp"

#include <algorithm>

//
// author: Kovacs Marton
// email: tetra666@gmail.com
// license: whatever. note my name
//
// remake of the great blaster screensaver, with more features i missed when watching it
// list of planned features:
//                            teams (so that red and green actually means something)
//                            score
//                            better(?) AI
//                            
//


//
// (ship : ammo) color theme for teams, 0 for default
//
Color teamColors[3][2] = {{Colors::red, Colors::green}, {Colors::red, Colors::green}, {Colors::blue, Colors::white}};

Wiz::Wiz()
{
  ships.push_back(new DiskShip(Coordinate(330, 300), Colors::red, *this, 1));
  ships.push_back(new DiskShip(Coordinate(70, 70), Colors::blue, *this, 2));
}

Wiz::~Wiz()
{
  delete ships[0];
}

void Wiz::DrawFrame()
{
  static int i=0;

  DrawCircle(Coordinate(200, 200), 100, Color(255, 125, 0), true);
  DrawCircle(Coordinate(210, 210), 100, Color(0, 255, 0), false);

  DrawLine(Coordinate(300 + i % 100, 300), Coordinate(400, 500), Color(0, 255, 255));

  Coordinate points[] = {Coordinate(100, 100), Coordinate(300, 100), Coordinate(300, 300), Coordinate(100, 300)};
  DrawShape(&points[0], &points[4], Color(0, 255, 0), false);
  ++i;

  MoveAll();
  Clean();
}

#include <iostream>

bool Wiz::CheckCollision(const Coordinate& begin, const Coordinate& end, int team)
{
  Coordinate vektor = end - begin;
  double len = Length(vektor);
  int steps = len / 2;
  for (int i = 0; i < steps; ++i)
  {
    Coordinate point = begin + vektor * 2 * steps / len;
    for(ShipList::iterator it = ships.begin(); ships.end() != it; ++it)
    {
      if ((0 == team || team != (*it)->GetTeam()) && Distance((*it)->GetCenter(), point) <= (*it)->GetSize())
      {
        std::cout << "ouch!\n";
        (*it)->Hit();
        return true;
      }
    }
  }
  return false;
}

void Wiz::AddProjectile(Flyer* projectile)
{
  projectiles.push_back(projectile);
}

void Wiz::RemoveProjectile(Flyer* projectile)
{
  ProjectileList::iterator iter = std::find(projectiles.begin(), projectiles.end(), projectile);
  if (projectiles.end() != iter)
  {
    deads.push_back(projectile);
  }
}

Coordinate Wiz::PlaceMe(int team)
{
  return Coordinate(70, 70);
}

void Wiz::MoveAll()
{
  //TODO: C++11 feature
  for(ShipList::iterator it = ships.begin(); ships.end() != it; ++it)
  {
    (*it)->Move();
    (*it)->Draw();
  }

  for(ProjectileList::iterator it = projectiles.begin(); projectiles.end() != it; ++it)
  {
    (*it)->Move();
    (*it)->Draw();
  }
}

void Wiz::Clean()
{
  for (ProjectileList::iterator it = deads.begin(); deads.end() != it; ++it)
  {
    KillProjectile(*it);
  }
  deads.clear();
}

void Wiz::KillProjectile(Flyer* projectile)
{
  ProjectileList::iterator iter = std::find(projectiles.begin(), projectiles.end(), projectile);
  if (projectiles.end() != iter)
  {
    delete *iter;
    projectiles.erase(iter);
  }
}

