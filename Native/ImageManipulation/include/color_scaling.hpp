//
// Created by dierck on 16.01.26.
//

#ifndef IMAGEMANIPULATION_COLOR_SCALING_HPP
#define IMAGEMANIPULATION_COLOR_SCALING_HPP

#include <opencv2/opencv.hpp>

namespace colorscale {
    cv::Mat scale_color(const cv::Mat& image, double factor);
    cv::Mat gamma_correction(const cv::Mat& image, double gamma);
}

#endif //IMAGEMANIPULATION_COLOR_SCALING_HPP