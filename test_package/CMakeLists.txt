project(helloworld)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

configure_file(qt.conf.in ${CMAKE_BINARY_DIR}/bin/qt.conf)

find_package(Qt5Core REQUIRED)

set(CMAKE_AUTOMOC ON)
set(AUTOMOC_MOC_OPTIONS PROPERTIES FOLDER CMakeAutomocTargets)
set_property(GLOBAL PROPERTY AUTOMOC_FOLDER CMakeAutomocTargets)

add_executable(helloworld main.cpp)
target_include_directories(helloworld PRIVATE ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(helloworld PUBLIC Qt5::Core)

add_subdirectory(hellogui)
