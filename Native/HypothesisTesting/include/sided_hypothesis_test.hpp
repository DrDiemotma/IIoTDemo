//
// Created by dierck on 18.08.25.
//

#ifndef HYPOTHESISTESTING_SIDED_HYPOTHESIS_TEST_HPP
#define HYPOTHESISTESTING_SIDED_HYPOTHESIS_TEST_HPP

#include <hypothesis_test.hpp>

template<typename T>
class SidedHypothesisTest : public HypothesisTest<T> {
public:
    explicit SidedHypothesisTest(const std::shared_ptr<const std::vector<T>> data) : HypothesisTest<T>(data) {}
    bool is_sided = true;
};

#endif //HYPOTHESISTESTING_SIDED_HYPOTHESIS_TEST_HPP