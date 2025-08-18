message(STATUS "Including tests")
include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/heads/main.zip
)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_executable(run_tests
        test_spearman_test.cpp
)

target_include_directories(run_tests PRIVATE ${PROJECT_SOURCE_DIR}/include)

target_link_libraries(run_tests
        PRIVATE
            gtest_main
            HypothesisTesting
)

include(GoogleTest)
gtest_discover_tests(run_tests)
