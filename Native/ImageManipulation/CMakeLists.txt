cmake_minimum_required(VERSION 4.0)
project(ImageManipulation LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)


# pybind11 - git
FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.12.0
)
FetchContent_MakeAvailable(pybind11)

# OpenCV - host installation
find_package(OpenCV REQUIRED)

add_library(colorscale STATIC
        src/color_scaling.cpp
)

target_include_directories(colorscale
        PUBLIC include
        PUBLIC ${OpenCV_INCLUDE_DIRS}
)

target_link_libraries(colorscale
        PRIVATE ${OpenCV_LIBS}
)

# create python module
pybind11_add_module(image_manipulation
        src/module.cpp
)

target_include_directories(image_manipulation
        PUBLIC ${OpenCV_INCLUDE_DIRS}
)

target_link_libraries(image_manipulation
        PRIVATE colorscale
)

