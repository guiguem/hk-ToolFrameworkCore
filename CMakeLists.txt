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
include(HKPackageBuilder)

hkbuilder_prepare_project()

include_directories(BEFORE
        ${PROJECT_SOURCE_DIR}/src/DataModel
#        ${PROJECT_SOURCE_DIR}/src/UserTools/DummyTool
#        ${PROJECT_SOURCE_DIR}/src/UserTools/Factory
#        ${PROJECT_SOURCE_DIR}/src/UserTools
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

#file(GLOB_RECURSE DATAMODEL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/DataModel/*.cpp")
#file(GLOB_RECURSE DUMMYTOOL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/UserTools/DummyTool/*.cpp")
#file(GLOB_RECURSE FACTORY_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/UserTools/Factory/*.cpp")
file(GLOB_RECURSE LOGGING_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Logging/*.cpp")
file(GLOB_RECURSE STORE_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Store/*.cpp")
file(GLOB_RECURSE TOOL_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/Tool/*.cpp")
file(GLOB_RECURSE TOOLCHAIN_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/ToolChain/*.cpp")
#file(GLOB EXE_SRC RELATIVE ${CMAKE_SOURCE_DIR} "src/src/*.cpp")


pbuilder_library(
        TARGET ToolFrameworkCore
        SOURCES ${STORE_SRC} ${TOOL_SRC} ${LOGGING_SRC}
        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
)


#pbuilder_library(
#        TARGET ToolChain
#        SOURCES ${TOOLCHAIN_SRC}
#        PROJECT_LIBRARIES ToolFrameworkCore
#        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
#        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
#)
# -> to be compiled later (needs user tools)
#pbuilder_library(
#        TARGET Factory
#        SOURCES ${FACTORY_SRC}
#        PROJECT_LIBRARIES
#        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
#        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
#)
#
#pbuilder_library(
#        TARGET DummyTool
#        SOURCES ${DUMMYTOOL_SRC}
#        PROJECT_LIBRARIES Tool
#        PUBLIC_EXTERNAL_LIBRARIES ${PUBLIC_EXT_LIBS}
#        PRIVATE_EXTERNAL_LIBRARIES ${PRIVATE_EXT_LIBS}
#)

pbuilder_install_headers(${HEADERS})

# Add the ToolChain source files as they are needed by each ToolApplication
pbuilder_install_files("${SRC_INSTALL_DIR}" ${TOOLCHAIN_SRC})

pbuilder_component_install_and_export(
        COMPONENT Library
        LIBTARGETS ToolFrameworkCore # ToolChain # Factory
)

#pbuilder_executables (
#        TARGETS_VAR toolmain
#        SOURCES ${EXE_SRC}
#        PROJECT_LIBRARIES ToolChain
#)

pbuilder_install_files(${PROJECT_SOURCE_DIR}/src/)