//
// Created by dierck on 14.08.25.
//

#ifndef HYPOTHESISTESTING_SPEARMAN_TEST_HPP
#define HYPOTHESISTESTING_SPEARMAN_TEST_HPP

#include <vector>
#include <sided_hypothesis_test.hpp>

// template class HypothesisTest<std::tuple<double, double>>;

/**
 * @brief Spearman test for correlation.
 *
 * Assume a bivariate population [(X_1, Y_1), ..., (X_N, Y_N)] with joint
 * distribution function F_{X,Y} and marginal distribution functions F_X, and F_Y.
 * The joint pairs (X_i, Y_i) are iid.
 *
 * Then the hypothesis is:
 *  - H_0: F_{X,Y}(x, y) === F_X(x) * F_Y(y)
 *  - H_1: F_{X,Y}(x, y) =/= F_X(x) * F_Y(y) (for at least one (x,y) pair)
 */
class SpearmanTest final : public SidedHypothesisTest<std::pair<double, double>> {
public:
    /**
     * Ranks for the Spearman hypothesis test. This uses coupled data and the difference between the
     * ranks to calculate the statistic.
     */
    struct Ranks {
        /**
         * Value pair for which the ranks are used.
         */
        const std::pair<double, double>& values;
        /**
         * Rank of the first element, that is values.first.
         */
        const double rank_item1;
        /**
         * Rank of the second element, that is values.second.
         */
        const double rank_item2;
        /**
         * Difference between the ranks.
         * @return rank_item2 - rank_item1
         */
        [[nodiscard]] double difference() const { return rank_item2 - rank_item1; }
    };

    /**
     * Data structure for the Spearman test.
     */
    using Data = std::vector<std::pair<double, double>>;  // std::vector to allocate on the heap. Might get big.

    explicit SpearmanTest(const std::shared_ptr<const Data>& data): SidedHypothesisTest(data){}

    const size_t CRITICAL_DIMENSION = 12;

    /**
     * Execute the Spearman test to test independence of two sequences.
     *
     */
    void execute_test() override;

    /**
     * Set the threshold > 0 by which two values are considered equal, that is, get the same rank.
     * @param threshold The threshold to set.
     */
    void set_equal_threshold(double threshold);

    /**
     * Get the calculated ranks
     * @return Ranks from the calculation
     */
    [[nodiscard]] std::vector<Ranks>& get_ranks()  { return m_ranks; }

    /**
     * Get the current threshold by which two values get the same rank.
     * @return The current threshold.
     */
    [[nodiscard]] double get_equal_threshold() const { return m_threshold; }

    [[nodiscard]] double get_correlation_coefficient() const {return m_correlation_coefficient; }

private:
    static void calculate_mid_ranks(std::vector<double>& min_set_ranks, double& max_rank);
    void calculate_ranks();
    double m_threshold = 10e-6;
    double m_correlation_coefficient = 0;
    std::vector<Ranks> m_ranks = std::vector<Ranks>();
};

#endif //HYPOTHESISTESTING_SPEARMAN_TEST_HPP
