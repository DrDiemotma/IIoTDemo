//
// Created by dierck on 16.01.26.
//

#include "color_scaling.hpp"

cv::Mat colorscale::scale_color(const cv::Mat& image, const double factor) {
    cv::Mat out;
    image.convertTo(out, -1, factor, 0);
    return out;
}

cv::Mat colorscale::gamma_correction(const cv::Mat &image, const double gamma) {
    cv::Mat out = image.clone();
    uchar lut[256];
    for (int i = 0; i < 256; ++i) {
        lut[i] = cv::saturate_cast<uchar>(std::pow(i / 255.0, gamma) * 255.0);
    }

    for (int row_index = 0; row_index < out.rows; ++row_index) {
        const auto row = out.ptr<uchar>(row_index);
        for (int x = 0; x < image.cols * image.channels(); ++x) {
            row[x] = lut[row[x]];
        }
    }

    return out;
}
