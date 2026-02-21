cmake_minimum_required(VERSION 3.16 FATAL_ERROR)
project(CR39_ProtonSim)

find_package(Geant4 REQUIRED ui_all vis_all)
include(${Geant4_USE_FILE})

include_directories(${PROJECT_SOURCE_DIR}/include)

file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

add_executable(CR39_sim main.cc ${sources} ${headers})
target_link_libraries(CR39_sim ${Geant4_LIBRARIES})

install(TARGETS CR39_sim DESTINATION bin)
