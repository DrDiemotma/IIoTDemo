//
// Created by dierck on 15.08.25.
//

#include <gtest/gtest.h>
#include <spearman_test.hpp>

TEST(spearman_test, SimplePerfectCorrelation) {

    const SpearmanTest::Data data = {
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
    };
    SpearmanTest test(data);
    test.execute_test();
    const auto result = test.is_significant();
    EXPECT_FALSE(result);
}

TEST(spearman_test, SimpleNotCorrelated) {
    // basically every value for item1 is paired with every value for item2 -> highly uncorrelated.
    const SpearmanTest::Data data = {
        {1.0, 1.0},
        {-1.0, 1.0},
        {1.0, -1.0},
        {-1.0, -1.0},
        {2.0, 1.0},
        {2.0, -1.0},
        {1.0, 2.0},
        {-1.0, 2.0},
        {2.0, 2.0},
        {-2.0, 1.0},
        {-2.0, -1.0},
        {1.0, -2.0},
        {-1.0, -2.0},
        {-2.0, -2.0},
        {2.0, -2.0},
        {-2.0, -2.0}
    };
     SpearmanTest test(data);
    test.execute_test();
    const auto result = test.is_significant();
    EXPECT_TRUE(result);
}