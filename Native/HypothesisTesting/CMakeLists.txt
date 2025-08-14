cmake_minimum_required(VERSION 4.0)
project(HypothesisTesting
        VERSION 0.0.0.1
        LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

option(HYPOTEST_BUILDS_TESTS "Build C++ unit tests" ON)
find_package(pybind11 CONFIG QUIET)
if (NOT pybind11_FOUND)
    message(STATUS "pybind11 not found")
else ()
    message(STATUS "pybind11 found")
endif ()

add_subdirectory(src)

if (HYPOTEST_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

