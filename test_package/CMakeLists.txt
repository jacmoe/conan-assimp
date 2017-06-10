project(PackageTest CXX)
cmake_minimum_required(VERSION 2.8.12)

set(CMAKE_DEBUG_POSTFIX "d")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(ZLIB REQUIRED)
INCLUDE_DIRECTORIES(${ZLIB_INCLUDE_DIR})

add_executable(example example.cpp)
target_link_libraries(example assimpd ${ZLIB_LIBRARIES})

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
