#include <iostream>
#include <cstdlib>
#include <ctime>

int main(int argc, char* argv[])
{
  int pool(std::atoi(argv[1]));
  int sample(std::atoi(argv[2]));
  const int poolOrig(pool + 1);

  std::srand(std::time(0));

  for (; pool > 0; --pool)
  {
    if (std::rand() % pool < sample)
    {
      std::cout << poolOrig - pool << '\n';
      --sample;
    }
  }
}

/*
 * int m,i;
 f *or(m=5,i=90;i>0;--i)
  if(rand()%i<m){
    printf("%d\n",91-i); --m;
  }
 */
