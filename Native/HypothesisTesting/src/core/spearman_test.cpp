//
// Created by dierck on 14.08.25.
//

#include <spearman_test.hpp>
#include <armadillo>

SpearmanTest::SpearmanTest() = default;

void SpearmanTest::execute_test(const std::vector<std::tuple<double, double> > &data) {
    set_data(data);
}

