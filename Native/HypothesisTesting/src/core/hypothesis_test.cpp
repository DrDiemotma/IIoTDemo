//
// Created by dierck on 14.08.25.
//

#include <hypothesis_test.hpp>
#include <sided_hypothesis_test.hpp>
#include <stdexcept>

template<typename T>
void HypothesisTest<T>::set_significance_level(const double alpha) {
    if (alpha < 0.0) {
        throw std::invalid_argument("alpha must be positive");
    }
    if (alpha > 1.0) {
        throw std::invalid_argument("alpha must be less than 1");
    }

    m_alpha = alpha;
}

template class HypothesisTest<std::pair<double, double>>;
template class HypothesisTest<std::pair<double, int>>;
template class SidedHypothesisTest<std::pair<double, double>>;
template class SidedHypothesisTest<std::pair<double, int>>;
