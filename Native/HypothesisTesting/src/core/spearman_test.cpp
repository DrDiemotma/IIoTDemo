//
// Created by dierck on 14.08.25.
//

#include <spearman_test.hpp>
#include <boost/math/distributions/students_t.hpp>
#include <numeric>

void SpearmanTest::execute_test() {
    const auto dimension = m_data->size();
    const auto scaling_factor = static_cast<double>(dimension * (dimension * dimension - 1));
    const auto ranks = calculate_ranks();
    double rank_difference_squared = 0;
    for (auto rank_tuple : ranks ) {
        const auto difference  = rank_tuple.difference();
        const auto difference_squared = difference * difference / scaling_factor;
        rank_difference_squared += difference_squared;
    }
    m_correlation_coefficient = 1.0 - 6 * rank_difference_squared;  // to formula, Pearson CC
    if (std::abs(std::abs(m_correlation_coefficient) - 1.0) < 10e-6) {
        // highly correlated, close to identical; nothing to decide here
        m_is_significant = false;
        return;
    }
    m_test_statistic = m_correlation_coefficient * sqrt(dimension - 2) /
        sqrt(1 - rank_difference_squared * rank_difference_squared);  // normalization to approx. x~t.

    const boost::math::students_t dist(dimension - 2);  // n-2 degrees of freedom for this test
    const double alpha = this->is_sided ? 1 - (1 - m_alpha) / 2 : m_alpha;
    const double t_quantile = boost::math::quantile(dist, alpha);
    m_is_significant = std::abs(m_test_statistic) > t_quantile;
}

std::vector<SpearmanTest::Ranks> SpearmanTest::calculate_ranks() const {
    std::vector<size_t> sort_indices1(m_data->size());
    std::vector<size_t> sort_indices2(m_data->size());
    std::iota(sort_indices1.begin(), sort_indices1.end(), 0);
    std::iota(sort_indices2.begin(), sort_indices2.end(), 0);
    Data& data_ref = *m_data;
    std::ranges::sort(sort_indices1,
        [data_ref](const size_t i1, const size_t i2) {
            return data_ref[i1].first < data_ref[i2].first;
    });
    std::ranges::sort(sort_indices2,
        [data_ref](const size_t i1, const size_t i2) {
            return data_ref[i1].second < data_ref[i2].second;
    });

    auto rank_x = 1.0;  // setting already to double to not have unnecessary casts
    auto rank_y = 1.0;  // setting already to double to not have unnecessary casts
    auto value_x = data_ref[sort_indices1[0]].first;
    auto value_y = data_ref[sort_indices2[0]].second;
    std::vector ranks_set1(data_ref.size(), 1.0);
    std::vector ranks_set2(data_ref.size(), 1.0);

    // first step: every element get the minimum rank possible to address
    for (int i = 1; i < data_ref.size(); ++i) {
        auto const current_x = data_ref[sort_indices1[i]].first;
        auto const current_y = data_ref[sort_indices2[i]].second;
        if (current_x - value_x > m_threshold) {  // current_x is always greater or equal because of the sort
            rank_x += 1.0;
        }
        if (current_y - value_y > m_threshold) {  // current_y is always greater or equal because of the sort
            rank_y += 1.0;
        }
        ranks_set1[sort_indices1[i]] = rank_x;
        ranks_set2[sort_indices2[i]] = rank_y;
        value_x = current_x;
        value_y = current_y;
    }

    // treating equal values: calculating the mid-rank
    calculate_mid_ranks(ranks_set1, rank_x);
    calculate_mid_ranks(ranks_set2, rank_y);

    std::vector<Ranks> ranks;
    ranks.reserve(data_ref.size());
    for (int i = 0; i < data_ref.size(); ++i) {
        Ranks current_rank{data_ref[i], ranks_set1[i], ranks_set2[i]};
        ranks.push_back(current_rank);
    }

    return ranks;
}

void SpearmanTest::set_equal_threshold(const double threshold) {
    if (threshold < 0.0) {
        throw std::invalid_argument("Threshold must be positive");
    }
    m_threshold = threshold;
}

void SpearmanTest::calculate_mid_ranks(std::vector<double>& min_set_ranks, double& max_rank) {
    const int n_elements = min_set_ranks.size();
    if (std::abs(n_elements - max_rank) < 10e-6) {  // no ties
        return;
    }
    double current_rank = 1.0;
    while (current_rank < max_rank) {
        std::vector<int> indices;
        std::vector<int> higher_ranks;
        for (int i = 0; i < n_elements; ++i) {
            if (std::abs(min_set_ranks[i] - current_rank) < 10e-8) {
                indices.push_back(i);
            }
            if (min_set_ranks[i] > current_rank + 10e-8) {
                higher_ranks.push_back(i);
            }
        }
        const int n_equals = indices.size();
        if (n_equals <= 1) {
            current_rank += 1.0;
            continue;
        }
        const double new_rank = (n_equals + 1.0) / 2.0 + current_rank - 1.0;
        for (const int i : indices) {
            min_set_ranks[i] = new_rank;
        }
        for (const int i : higher_ranks) {
            min_set_ranks[i] = min_set_ranks[i] + n_equals - 1.0;
        }
        max_rank += n_equals - 1.0;
        current_rank += n_equals;
    }
}
