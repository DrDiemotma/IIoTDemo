//
// Created by dierck on 14.08.25.
//

#ifndef HYPOTHESISTESTING_SPEARMAN_TEST_HPP
#define HYPOTHESISTESTING_SPEARMAN_TEST_HPP

#include <vector>

#include "hypothesis_test.hpp"


/**
 * @brief Spearman test for independence.
 *
 * Assume a bivariate population [(X_1, Y_1), ..., (X_N, Y_N)] with joint
 * distribution function F_X,X and marginal distribution functions F_X, and F_Y.
 * The joint pairs X_i, Y_i are iid.
 *
 * Then the hypothesis is:
 *  - H_0: F_X,Y(x, y) === F_X(x) * F_Y(y)
 *  - H_1: F_X,Y(x, y) =/= F_X(x) * F_Y(y) (for at least one (x,y) pair)
 */
class SpearmanTest : HypothesisTest<std::tuple<double, double>> {
public:
    /**
     * ctor.
     */
    SpearmanTest();

    /**
     * Execute the Spearman test to test independence of two sequences.
     *
     * @param data Tuples of data from the population.
     */
    void execute_test(const std::vector<std::tuple<double, double>> &data) override;
};

#endif //HYPOTHESISTESTING_SPEARMAN_TEST_HPP