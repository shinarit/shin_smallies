#include <cstring>

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
      return m_data[m_currRow * m_size + m_currColumn];
    }
    
    MatrixExcludeIterator& operator++()
    {
      ++m_currColumn;
      if (m_size == m_currColumn)
      {
        m_currColumn = 0;
        ++m_currRow;
      }

      if (m_columnToExclude == m_currColumn)
      {
        ++m_currColumn;
        if (m_size == m_currColumn)
        {
          m_currColumn = 0;
          ++m_currRow;
        }
      }

      if (m_rowToExclude == m_currRow)
      {
        ++m_currRow;
      }
    }
    
    MatrixExcludeIterator operator++(int)
  
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
      for (int i(0); i < size * size; ++i;)
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
          return  a[1][1]*a[2][2]*a[3][3] + a[1][2]*a[2][3]*a[3][1] + a[1][3]*a[2][1]*a[3][2] -
                  a[3][1]*a[2][2]*a[1][3] - a[3][2]*a[2][3]*a[1][1] - a[3][3]*a[2][1]*a[1][2];
        }
        default:
        {
          ValueType res;
          
          
          
          return res;
        }
      }
    }

  private:
    int         m_size;
    ValueType*  m_data;    
};


int main()
{
}

