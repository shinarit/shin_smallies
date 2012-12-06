#include <cstdlib>
#include <cstdint>
#include <iostream>
#include <vector>
#include <algorithm>
#include <map>

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
    out << groupSize - 1 - res.getResult(i) << " : " << res.getResult(i) << '\n';
  }
  return out;
}

int main(int argc, char* argv[])
{
  int groupSize(std::atoi(argv[1]));

  uint64_t max(1 << ((groupSize * (groupSize - 1) / 2)));

  std::cout << "max: " << max << '\n';
  std::map<Result, int> results;
  for (uint64_t i(0); i < max; ++i)
  {
    ++results[Result(groupSize, i)];
  }

  std::vector<std::pair<int, Result>> swappedVector;
  std::transform(begin(results), end(results), std::back_inserter<std::vector<std::pair<int, Result>>>(swappedVector), [](std::pair<Result, int> pair) {return std::make_pair(pair.second, pair.first);});
  std::sort(begin(swappedVector), end(swappedVector));

  std::cout << "number of results: " << results.size() << '\n';

  for (const auto& result: swappedVector)
  {
    std::cout << "occurrence: " << result.first << ", percent: " << result.first * 100.0f / max << '\n';
    std::cout << result.second << '\n';
  }
}
