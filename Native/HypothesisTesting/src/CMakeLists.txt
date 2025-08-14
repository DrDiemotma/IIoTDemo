add_library(hypotest_core
        ../include/spearman_test.hpp
        core/spearman_test.cpp
        ../include/hypothesis_test.hpp
        core/hypothesis_test.cpp
)

target_include_directories(hypotest_core PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_compile_features(hypotest_core PUBLIC cxx_std_20)


# pybind11_add_module(_hypotest bindings/python_bindings.cpp)
# target_link_libraries(_hypotest PRIVATE hypotest_core)
# set_target_properties(_hypotest PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/python)