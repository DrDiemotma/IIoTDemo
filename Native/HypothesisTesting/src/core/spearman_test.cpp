//
// Created by dierck on 14.08.25.
//

#include <spearman_test.hpp>
#include <boost/math/distributions/students_t.hpp>
#include <numeric>


void SpearmanTest::execute_test() {
    const auto dimension = static_cast<double>(m_data->size());
    if (dimension < static_cast<double>(CriticalDimension)) {
        throw std::invalid_argument("Sample size must be greater than CRITICAL_DIMENSION");
    }
    const auto ln_dim = std::log(dimension);
    const auto ln_dim_neg = std::log(dimension - 1.0);
    const auto ln_dim_pos = std::log(dimension + 1.0);
    const auto scaling_factor = dimension < 10e17
        ? std::sqrt(dimension * (dimension - 1.0) * (dimension + 1.0))
        : std::exp(0.5 * (ln_dim + ln_dim_neg + ln_dim_pos));
    calculate_ranks();

    // see M. Hollander et al., "Nonparametric Statistical Methods", Third Edition, p. 428, (8.64)
    double rank_difference_squared = 0;
    for (auto rank_tuple : m_ranks ) {
        const auto difference_normalized  = rank_tuple.difference() / scaling_factor;
        const auto difference_squared = difference_normalized * difference_normalized;
        rank_difference_squared += difference_squared;
    }
    m_correlation_coefficient = 1.0 - 6 * rank_difference_squared;  // to formula, Pearson CC
    if (std::abs(std::abs(m_correlation_coefficient) - 1.0) < 10e-6) {
        // highly correlated, close to identical; nothing to decide here
        m_is_significant = true;
        m_p_value = 0.0;
        return;
    }
    const auto degrees_of_freedom = static_cast<double>(dimension - 2);
    m_test_statistic = m_correlation_coefficient * sqrt(degrees_of_freedom) /
        sqrt(1 - m_correlation_coefficient * m_correlation_coefficient);  // normalization to approx. x~t.

    const boost::math::students_t dist(static_cast<double>(dimension - 2));  // n-2 degrees of freedom for this test
    const double sided_p_value = 2.0 * (1.0 - boost::math::cdf(dist, std::fabs(m_test_statistic)));
    m_p_value = is_sided ? sided_p_value : 2 * sided_p_value;

    const double q = is_sided ? 1 - m_alpha : 1 - m_alpha / 2;
    const double quantile = boost::math::quantile(dist, q);
    m_is_significant = std::fabs(m_test_statistic) >= quantile;
}

void SpearmanTest::calculate_ranks() {
    std::vector<size_t> sort_indices1(m_data->size());
    std::vector<size_t> sort_indices2(m_data->size());
    std::iota(sort_indices1.begin(), sort_indices1.end(), 0);
    std::iota(sort_indices2.begin(), sort_indices2.end(), 0);
    const Data& data_ref = *m_data;
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

    m_ranks.clear();
    m_ranks.reserve(data_ref.size());
    for (int i = 0; i < data_ref.size(); ++i) {
        Ranks current_rank{data_ref[i], ranks_set1[i], ranks_set2[i]};
        m_ranks.push_back(current_rank);
    }
}

void SpearmanTest::set_equal_threshold(const double threshold) {
    if (threshold < 0.0) {
        throw std::invalid_argument("Threshold must be positive");
    }
    m_threshold = threshold;
}

void SpearmanTest::calculate_mid_ranks(std::vector<double>& min_set_ranks, double& max_rank) {
    const auto n_elements = static_cast<double>(min_set_ranks.size());  // treated as double for the rank calculation
    if (std::abs(n_elements - max_rank) < 10e-6) {  // no ties
        return;
    }
    double current_rank = 1.0;
    while (current_rank < max_rank + 1 / n_elements) { // ranks are mitigated between the elements -> exceeding that breaks the loop
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
        const auto n_equals = static_cast<double>(indices.size());  //used several times as double later on
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
