file(GLOB_RECURSE SOURCES "*.cpp" "*.hpp")

add_library (SpeechRecognitionModule SHARED ${SOURCES})

target_include_directories(SpeechRecognitionModule PRIVATE ${SC_MEMORY_SRC})
target_link_libraries(SpeechRecognitionModule sc-memory)

add_dependencies(SpeechRecognitionModule sc-memory)

sc_codegen(SpeechRecognitionModule ${CMAKE_CURRENT_LIST_DIR})