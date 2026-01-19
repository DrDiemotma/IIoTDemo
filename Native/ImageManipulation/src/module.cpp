//
// Created by dierck on 16.01.26.
//

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

#include "color_scaling.hpp"

namespace py = pybind11;

py::array_t<uint8_t> py_scale_color(const py::array_t<uint8_t>& input, const double factor) {
    const py::buffer_info info = input.request();
    if (info.ndim != 3 || info.shape[2] != 3) {
        throw std::runtime_error("Expected an RGB image with shape (height x width x 3)");
    }

    const auto height = static_cast<int>(info.shape[0]);
    const auto width = static_cast<int>(info.shape[1]);

    const cv::Mat img(height, width, CV_8UC3, info.ptr);
    const cv::Mat out = colorscale::scale_color(img, factor);

    auto result = py::array_t<uint8_t>({height, width, 3});
    const py::buffer_info out_info = result.request();
    const auto out_ptr = static_cast<uint8_t*>(out_info.ptr);
    memcpy(out_ptr, out.data, height * width * 3);

    return result;
}

py::array_t<uint8_t> py_gamma(const py::array_t<uint8_t>& input, const double gamma) {
    const py::buffer_info info = input.request();
    if (info.ndim != 3 || info.shape[2] != 3) {
        throw std::runtime_error("Expected an RG image with shape (height x width x 3)");
    }

    const auto height = static_cast<int>(info.shape[0]);
    const auto width = static_cast<int>(info.shape[1]);

    const cv::Mat img(height, width, CV_8UC3, info.ptr);
    const cv::Mat out = colorscale::gamma_correction(img, gamma);

    auto result = py::array_t<uint8_t>({height, width, 3});
    const py::buffer_info out_info = result.request();
    const auto out_ptr = static_cast<uint8_t*>(out_info.ptr);
    memccpy(out_ptr, out.data, height * width * 3, out_info.ndim);

    return result;
}

PYBIND11_MODULE(image_manipulation, m) {
    m.doc() = "Python bindings for image manipulation in OpenCV";

    m.def(
        "scale_color",
        &py_scale_color,
        "Scales the color of an image"
        );

    m.def(
        "gamma_correction",
        &py_gamma,
        "Gamma correction for an image."
        );
}