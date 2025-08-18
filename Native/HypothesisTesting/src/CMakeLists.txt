add_library(HypothesisTesting
        core/spearman_test.cpp
        core/hypothesis_test.cpp
)

target_include_directories(HypothesisTesting PUBLIC ${PROJECT_SOURCE_DIR}/include)
target_compile_features(HypothesisTesting PUBLIC cxx_std_20)


# pybind11_add_module(_hypotest bindings/python_bindings.cpp)
# target_link_libraries(_hypotest PRIVATE HypothesisTesting)
# set_target_properties(_hypotest PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/python)