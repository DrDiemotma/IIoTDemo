//
// Created by dierck on 14.08.25.
//

#include <hypothesis_test.hpp>

template<typename T>
void HypothesisTest<T>::set_data(const std::vector<T> &data) {
    m_data.clear();
    m_data.insert(m_data.end(), data.begin(), data.end());
    m_is_significant = false;
    m_test_statistic = 0.0;
}

template<typename T>
bool HypothesisTest<T>::is_significant() const {
    return m_is_significant;
}


