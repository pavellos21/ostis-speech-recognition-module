file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (SRMTest SHARED ${SOURCES})

target_include_directories(SRMTest PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(SRMTest sc-memory)

add_dependencies(SRMTest sc-memory)

sc_codegen(SRMTest ${CMAKE_CURRENT_LIST_DIR})