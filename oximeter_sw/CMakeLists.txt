# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# initalize pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "C:/Users/Anton/Documents/Pico/pico-sdk")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(oximeter_sw C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(oximeter_sw oximeter_sw.c )

pico_set_program_name(oximeter_sw "oximeter_sw")
pico_set_program_version(oximeter_sw "0.1")

pico_enable_stdio_uart(oximeter_sw 1)
pico_enable_stdio_usb(oximeter_sw 0)

# Add the standard library to the build
target_link_libraries(oximeter_sw pico_stdlib hardware_adc hardware_gpio)

pico_add_extra_outputs(oximeter_sw)

