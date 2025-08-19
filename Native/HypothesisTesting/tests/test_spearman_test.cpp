//
// Created by dierck on 15.08.25.
//

#include <gtest/gtest.h>
#include <spearman_test.hpp>
#include <numeric>

std::shared_ptr<const SpearmanTest::Data> generate_independent_test_data(const int min, const int max) {
    std::vector<double> span;
    span.reserve(max - min + 1);
    for (int i = min; i <= max; ++i) {
        span.push_back(i);
    }

    auto data = std::make_shared<SpearmanTest::Data>();
    data->reserve(span.size() * span.size());
    for (size_t i = 0; i < span.size(); ++i) {
        for (size_t j = 0; j < span.size(); ++j) {
            data->emplace_back(span[i], span[j]);
        }
    }

    return data;
}

TEST(spearman_test, SimplePerfectCorrelation) {

    const auto data = std::make_shared<SpearmanTest::Data>(SpearmanTest::Data{
        {1.0, 1.0},
        {2.0, 2.0},
        {3.0, 3.0},
        {4.0, 4.0},
        {5.0, 5.0},
        {6.0, 6.0},
        {7.0, 7.0},
        {8.0, 8.0},
        {9.0, 9.0},
        {10.0, 10.0}
    });
    SpearmanTest test(data);
    test.execute_test();
    const auto result = test.is_significant();
    EXPECT_FALSE(result);
}

TEST(spearman_test, SimpleRanks) {
    const auto data = generate_independent_test_data(1, 2);
    SpearmanTest test(data);
    test.execute_test();
    auto const ranks = test.get_ranks();
    // item1: [1, 1, 2, 2] => ranks[:].rank_item1 should be 1.5, 1.5, 3.5, 3.5
    EXPECT_LE(std::abs(ranks[0].rank_item1 - 1.5), 10e-8);
    EXPECT_LE(std::abs(ranks[1].rank_item1 - 1.5), 10e-8);
    EXPECT_LE(std::abs(ranks[2].rank_item1 - 3.5), 10e-8);
    EXPECT_LE(std::abs(ranks[3].rank_item1 - 3.5), 10e-8);
    // item2: [1, 2, 1, 2]
    EXPECT_LE(std::abs(ranks[0].rank_item2 - 1.5), 10e-8);
    EXPECT_LE(std::abs(ranks[1].rank_item2 - 3.5), 10e-8);
    EXPECT_LE(std::abs(ranks[2].rank_item2 - 1.5), 10e-8);
    EXPECT_LE(std::abs(ranks[3].rank_item2 - 3.5), 10e-8);
}

TEST(spearman_test, ComplexRanks) {
    const auto data_threefold = generate_independent_test_data(1, 3);
    SpearmanTest test_threefold(data_threefold);
    test_threefold.execute_test();
    auto const ranks = test_threefold.get_ranks();
    // item1: [1, 1, 1, 2, 2, 2, 3, 3, 3] => ranks[:].rank_item1 should be 2, 2, 2, 5, 5, 5, 8, 8, 8
    EXPECT_LE(std::abs(ranks[0].rank_item1 - 2.0), 10e-8);
    EXPECT_LE(std::abs(ranks[1].rank_item1 - 2.0), 10e-8);
    EXPECT_LE(std::abs(ranks[2].rank_item1 - 2.0), 10e-8);
    EXPECT_LE(std::abs(ranks[3].rank_item1 - 5.0), 10e-8);
    EXPECT_LE(std::abs(ranks[4].rank_item1 - 5.0), 10e-8);
    EXPECT_LE(std::abs(ranks[5].rank_item1 - 5.0), 10e-8);
}

TEST(spearman_test, SimpleNotCorrelated) {
    const auto data = generate_independent_test_data(1, 2);
    SpearmanTest test(data);
    test.is_sided = false;
    test.execute_test();
    const auto result = test.is_significant();
    EXPECT_TRUE(result);
}