# Minimum cmake verison 3.1 required for the variable CMAKE_CXX_STANDARD
cmake_minimum_required(VERSION 3.1)

set(PROJECT_NAME hk-ToolFrameworkCore)
set(PROJECT_VERSION 1.0.0)


project(${PROJECT_NAME} VERSION ${PROJECT_VERSION})

set(default_build_type "Release")
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
    set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE
            STRING "Choose the type of build." FORCE)
    # Set the possible values of build type for cmake-gui
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS
            "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif ()

list(APPEND CMAKE_MODULE_PATH
        $ENV{HK_PILOT_DIR}/cmake
        )
MESSAGE(STATUS ${CMAKE_MODULE_PATH})
include(PackageBuilder)

pbuilder_prepare_project()

MACRO(HEADER_DIRECTORIES return_list)
    FILE(GLOB_RECURSE new_list ${PROJECT_SOURCE_DIR}/*.h)
    FILE(COPY ${new_list} DESTINATION ${PROJECT_BINARY_DIR}/include)
    SET(dir_list "")
    FOREACH(file_path ${new_list})
        GET_FILENAME_COMPONENT(dir_path ${file_path} PATH)
        SET(dir_list ${dir_list} ${dir_path})
    ENDFOREACH()
    LIST(REMOVE_DUPLICATES dir_list)
    SET(${return_list} ${dir_list})
ENDMACRO()


include_directories(BEFORE
        ${PROJECT_SOURCE_DIR}/src/DataModel
        ${PROJECT_SOURCE_DIR}/src/UserTools/DummyTool
        ${PROJECT_SOURCE_DIR}/src/UserTools/Factory
        ${PROJECT_SOURCE_DIR}/src/UserTools
        ${PROJECT_SOURCE_DIR}/src/src/Logging
        ${PROJECT_SOURCE_DIR}/src/src/Store
        ${PROJECT_SOURCE_DIR}/src/src/Tool
        ${PROJECT_SOURCE_DIR}/src/src/ToolChain
        )

######################
#   Core             #
######################
# If there were other libraries in this package on which this library depends, then they would be put in this variable
set(PACKAGE_LIBS )


FILE(GLOB_RECURSE HEADERS
        ${PROJECT_SOURCE_DIR}/src/DataModel/*.h
        ${PROJECT_SOURCE_DIR}/src/UserTools/Factory/Factory.h
        ${PROJECT_SOURCE_DIR}/src/UserTools/DummyTool/DummyTool.h
        ${PROJECT_SOURCE_DIR}/src/UserTools/Unity.h
        ${PROJECT_SOURCE_DIR}/src/src/Logging/*.h
        ${PROJECT_SOURCE_DIR}/src/src/Store/*.h
        ${PROJECT_SOURCE_DIR}/src/src/Tool/*.h
        ${PROJECT_SOURCE_DIR}/src/src/ToolChain/*.h
        )
MESSAGE(STATUS ${HEADERS})

file(GLOB_RECURSE DATAMODEL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/DataModel/*.cpp")
file(GLOB_RECURSE DUMMYTOOL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/UserTools/DummyTool/*.cpp")
file(GLOB_RECURSE FACTORY_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/UserTools/Factory/*.cpp")
file(GLOB_RECURSE LOGGING_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Logging/*.cpp")
file(GLOB_RECURSE STORE_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Store/*.cpp")
file(GLOB_RECURSE TOOL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Tool/*.cpp")
file(GLOB_RECURSE TOOLCHAIN_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/ToolChain/*.cpp")
file(GLOB EXE_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/*.cpp")

pbuilder_library(
        TARGET Store
        SOURCES ${STORE_SRC}
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)


pbuilder_library(
        TARGET CoreDataModel
        SOURCES ${DATAMODEL_SRC}
        PROJECT_LIBRARIES Store
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_library(
        TARGET Logging
        SOURCES ${LOGGING_SRC}
        PROJECT_LIBRARIES ${PACKAGE_LIBS}
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_library(
        TARGET Tool
        SOURCES ${TOOL_SRC}
        PROJECT_LIBRARIES CoreDataModel
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_library(
        TARGET ToolChain
        SOURCES ${TOOLCHAIN_SRC}
        PROJECT_LIBRARIES Logging Factory
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_library(
        TARGET Factory
        SOURCES ${FACTORY_SRC}
        PROJECT_LIBRARIES DummyTool
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_library(
        TARGET DummyTool
        SOURCES ${DUMMYTOOL_SRC}
        PROJECT_LIBRARIES Tool
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)

pbuilder_install_headers(${HEADERS})


#add_subdirectory(src)

pbuilder_component_install_and_export(
        COMPONENT Library
        LIBTARGETS Store CoreDataModel Logging  Tool ToolChain Factory DummyTool
)

MESSAGE(${EXE_SRC})
pbuilder_executables (
        TARGETS_VAR toolmain
        SOURCES ${EXE_SRC}
        PROJECT_LIBRARIES ToolChain
)



#configure_file(this_myhklib.sh.in this_myhklib.sh)
#pbuilder_install_files(${BIN_INSTALL_DIR} ${CMAKE_CURRENT_BINARY_DIR}/this_ptheta.sh)

configure_file(${PROJECT_SOURCE_DIR}/${PROJECT_NAME}Config.cmake.in ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake @ONLY)
pbuilder_do_package_config()

add_custom_target(install_${PROJECT_NAME}
        "${CMAKE_COMMAND}" --build "${CMAKE_BINARY_DIR}" --target install
        COMMENT "Installing ${PROJECT_NAME}")
