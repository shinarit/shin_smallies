#include <iostream>
#include <vector>
#include <cstring>
#include <cstdlib>

typedef int ValueType;

class Line
{
  public:
    Line(ValueType* values): m_data(values)
    { }
    
    ValueType& operator[](int index)
    {
      return m_data[index];
    }

  private:
    ValueType* m_data;
};

class MatrixExcludeIterator
{
  public:
    MatrixExcludeIterator(int size, ValueType* data, int row, int column):  m_size(size), m_data(data), m_rowToExclude(row), m_columnToExclude(column), m_currIndex(-1)
    {
      Increment();
    }
    
    ValueType& operator*()
    {
      return m_data[m_currIndex];
    }
    
    MatrixExcludeIterator& operator++()
    {
      Increment();
      return *this;
    }
    
    MatrixExcludeIterator operator++(int)
    {
      MatrixExcludeIterator tmp = *this;
      Increment();
      return tmp;
    }
  
  private:
    void Increment()
    {
      ++m_currIndex;
      if (m_currIndex % m_size == m_columnToExclude)
      {
        ++m_currIndex;
      }
      if (m_currIndex / m_size == m_rowToExclude)
      {
        m_currIndex = m_size * (m_rowToExclude + 1);
      }
      if (m_currIndex % m_size == m_columnToExclude)
      {
        ++m_currIndex;
      }
    }
  
    const int   m_size;
    ValueType*  m_data;
    const int   m_rowToExclude;
    const int   m_columnToExclude;
    int         m_currIndex;
};

class SquareMatrix
{
  public:
    SquareMatrix(int size, ValueType* values): m_size(size), m_data(new ValueType[size * size])
    {
      std::memcpy(m_data, values, size * size * sizeof(ValueType));
    }
    template<class Iter>
    SquareMatrix(int size, Iter begin): m_size(size), m_data(new ValueType[size * size])
    {
      ValueType* runptr = &m_data[0];
      for (int i(0); i < size * size; ++i)
      {
        *runptr++ = *begin++;
      }
    }
    
    ~SquareMatrix()
    {
      delete m_data;
    }

    Line operator[](int index)
    {
      return &m_data[index * m_size];
    }
    
    ValueType Determinant()
    {
      switch (m_size)
      {
        case 1:
        {
          return m_data[0];
        }
        case 2:
        {
          return m_data[0] * m_data[3] - m_data[1] * m_data[2];
        }
        case 3:
        {
          //sarrus
          SquareMatrix& a = *this;
          return  a[0][0]*a[1][1]*a[2][2] + a[0][1]*a[1][2]*a[2][0] + a[0][2]*a[1][0]*a[2][1] -
                  a[2][0]*a[1][1]*a[0][2] - a[2][1]*a[1][2]*a[0][0] - a[2][2]*a[1][0]*a[0][1];
        }
        default:
        {
          ValueType res = 0;
          
          int sign = 1;
          for (int i(0); i<m_size; ++i)
          {
            res += sign * m_data[i] * Determinant(0, i);

            sign *= -1;
          }
          
          return res;
        }
      }
    }
    
    ValueType Determinant(int row, int column)
    {
      if (1 == m_size || row > m_size || column > m_size)
      {
        throw -1;
			}
			
			SquareMatrix tmp(m_size - 1, MatrixExcludeIterator(m_size, m_data, row, column));//.Determinant();
      return tmp.Determinant();
		}
		
		void Print() const
		{
			for (int i(0); i < m_size * m_size; ++i)
			{
				std::cout << m_data[i];
				if (m_size - 1 == i % m_size)
					std::cout << '\n';
				else
					std::cout << ' ';
			}
		}

  private:
    int         m_size;
    ValueType*  m_data;    
};


int main(int argc, char* argv[])
{
	if (2 != argc)
	{
		std::cout << "usage: " << argv[0] << " <dimension of vectors>\n";
	}
  int size = std::atoi(argv[1]);
	
  std::vector<ValueType> vec(size);
  for (int i(0); i < size * (size - 1); ++i)
  {
		ValueType num;
    std::cin >> num;
    vec.push_back(num);
  }
  
  SquareMatrix matr(size, &vec[0]);
  
  std::cout << '(';
  int sign = 1;
  for (int i(0); i < size - 1; ++i)
  {
		std::cout << sign * matr.Determinant(0, i) << ", ";
		sign *= -1;
	}
  std::cout << sign * matr.Determinant(0, size - 1) << ")\n";
}

