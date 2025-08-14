//
// Created by dierck on 14.08.25.
//

#ifndef HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP
#define HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP
#include <vector>

template<typename T>
class HypothesisTest {
public:
    /**
     * Execute the test.
     * @param data Data to perform the test on.
     */
    virtual void execute_test(const std::vector<T> &data) = 0;

    /**
     * Get whether the test was executed and rejected the default hypothesis (H_0).
     * @return Whether the default hypothesis can be rejected. Notice that before computation, this is always false.
     */
    [[nodiscard]] bool is_significant() const;

    /**
     * dtor.
     */
    virtual ~HypothesisTest() = default;
protected:
    std::vector<T> m_data;
    /**
     * Set the data in memory for potential recalculation.
     */
    virtual void set_data(const std::vector<T> &data);
    bool m_is_significant = false;
    double m_test_statistic = 0.0;
};

#endif //HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP