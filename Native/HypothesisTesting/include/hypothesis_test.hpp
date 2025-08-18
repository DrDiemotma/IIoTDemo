//
// Created by dierck on 14.08.25.
//

#ifndef HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP
#define HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP
#include <memory>
#include <vector>

template<typename T>
class HypothesisTest {
public:
    explicit HypothesisTest(const std::shared_ptr<std::vector<T>> data) : m_data(data) {}
    /**
     * Execute the test.
     */
    virtual void execute_test() = 0;

    /**
     * Get whether the test was executed and rejected the default hypothesis (H_0).
     * @return Whether the default hypothesis can be rejected. Notice that before computation, this is always false.
     */
    [[nodiscard]] bool is_significant() const {return m_is_significant;};

    /**
     * Set the significance level of the test. Default value is 0.95.
     * @param alpha parameter [0..1].
     */
    void set_significance_level(double alpha);

    /**
     * Get the currently set significance level.
     * @return the currently set significance level.
     */
    [[nodiscard]] double get_significance_level() const {return m_alpha;};

    /**
     * dtor.
     */
    virtual ~HypothesisTest() = default;
protected:
    const std::shared_ptr<std::vector<T>> m_data;
    /**
     * Set the data in memory for potential recalculation. Resets all evaluations.
     */
    bool m_is_significant = false;
    /**
     * Set the test statistic with is compared to m_alpha to evaluate whether the test is significant.
     */
    double m_test_statistic = 0.0;
    /**
     * Significance level.
     */
    double m_alpha = 0.95;
};

#endif //HYPOTHESISTESTING_HYPOTHESIS_TEST_HPP