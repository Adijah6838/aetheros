cmake_minimum_required(VERSION 3.14)
project(AetherEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# Fetch Dependencies
FetchContent_Declare(cpp_httplib GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git GIT_TAG v0.15.3)
FetchContent_Declare(json GIT_REPOSITORY https://github.com/nlohmann/json.git GIT_TAG v3.11.3)
FetchContent_Declare(googletest GIT_REPOSITORY https://github.com/google/googletest.git GIT_TAG v1.14.0)

FetchContent_MakeAvailable(cpp_httplib json googletest)

# Main Server Executable
add_executable(aether_engine src/main.cpp)
target_link_libraries(aether_engine PRIVATE httplib::httplib nlohmann_json::nlohmann_json)
target_include_directories(aether_engine PRIVATE include)

# Tests Executable
enable_testing()
add_executable(engine_tests tests/test_allocation.cpp)
target_link_libraries(engine_tests PRIVATE GTest::gtest_main)
target_include_directories(engine_tests PRIVATE include)
add_test(NAME EngineTests COMMAND engine_tests)