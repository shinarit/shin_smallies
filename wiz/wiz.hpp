//
// author: Kovacs Marton
// email: tetra666@gmail.com
// license: whatever. note my name
//
// wiz.hpp
//
// the main class that represents and moves the draw logic
//

#ifndef WIZ_HPP
#define WIZ_HPP

#include <vector>

class Flyer;
class Hitable;
class Coordinate;

class Wiz
{
  public:
    Wiz();
    ~Wiz();
    void DrawFrame();
    bool CheckCollision(const Coordinate& begin, const Coordinate& end, int team = 0) const;
    void AddProjectile(Flyer*);
    void RemoveProjectile(Flyer*);
    Coordinate PlaceMe(int team) const;

    typedef std::vector<const Hitable*> ShipTravel;
    ShipTravel GetEnemies(int team) const;

  private:
    void MoveAll();
    void Clean();
    void KillProjectile(Flyer*);

    typedef std::vector<Hitable*> ShipList;
    ShipList ships;

    typedef std::vector<Flyer*> ProjectileList;
    ProjectileList projectiles;

    ProjectileList deads;
};

#endif // WIZ_HPP
