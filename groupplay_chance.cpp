#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <set>

class Result
{
public:
  Result(int groupSize, uint64_t result): m_result(groupSize)
  {
    uint64_t runPtr = 1;
    int max(groupSize * (groupSize - 1) / 2);
    for (int i(0); i < groupSize; ++i)
    {
      for (int j(0); j < i; ++j)
      {
        if (result & runPtr)
        {
          ++m_result[j];
        }
        else
        {
          ++m_result[i];
        }

        runPtr <<= 1;
      }
    }
    std::sort(begin(m_result), end(m_result));
  }
  int getResult(int teamId) const
  {
    return m_result[teamId];
  }
  int groupSize() const
  {
    return m_result.size();
  }

private:
  friend bool operator<(const Result& lhs, const Result& rhs);
  std::vector<int> m_result;
};

bool operator<(const Result& lhs, const Result& rhs)
{
  return lhs.m_result < rhs.m_result;
}

std::ostream& operator<<(std::ostream& out, const Result& res)
{
  int groupSize(res.groupSize());
  for (int i(0); i < groupSize; ++i)
  {
    out << res.getResult(i) << " : " << groupSize - 1 - res.getResult(i) << '\n';
  }
  return out;
}

int main(int argc, char* argv[])
{
  int groupSize(std::atoi(argv[1]));

  uint64_t max(1 << ((groupSize * (groupSize - 1) / 2)));

  std::cout << "max: " << max << '\n';
  std::set<Result> results;
  for (uint64_t i(0); i < max; ++i)
  {
    results.insert(Result(groupSize, i));
  }
  std::cout << "number of results: " << results.size() << '\n';
  for (const auto& result: results)
  {
    std::cout << result << '\n';
  }
}
