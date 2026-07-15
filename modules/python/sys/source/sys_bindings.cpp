/*
 * =========================================================================
 * This file is part of sys-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * sys-python is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; If not,
 * see <http://www.gnu.org/licenses/>.
 *
 */

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

// CODA-OSS sys module headers
#include "sys/Conf.h"
#include "sys/UTCDateTime.h"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(coda_sys, m) {
    m.doc() = "Python bindings for CODA-OSS sys module (nanobind implementation)";
    
    // ========================================================================
    // CONSTANTS
    // ========================================================================
    
    m.attr("SSE_INSTRUCTION_ALIGNMENT") = sys::SSE_INSTRUCTION_ALIGNMENT;
    m.attr("NativeLayer_func__") = NativeLayer_func__;
    m.attr("SYS_FUNC") = SYS_FUNC;
    
    // ========================================================================
    // FUNCTIONS
    // ========================================================================
    
    // isBigEndianSystem
    m.def("isBigEndianSystem", &sys::isBigEndianSystem,
          "Check if the system uses big-endian byte order.\n\n"
          "Returns:\n"
          "    bool: True if big-endian, False if little-endian");
    
    // byteSwap - in-place version
    m.def("byteSwap",
          [](nb::capsule buffer, unsigned short elemSize, size_t numElems) {
              void* ptr = buffer.data();
              sys::byteSwap(ptr, elemSize, numElems);
          },
          "buffer"_a, "elemSize"_a, "numElems"_a,
          "Byte swap data in-place.\n\n"
          "Args:\n"
          "    buffer: Memory buffer containing data to swap\n"
          "    elemSize: Size of each element in bytes\n"
          "    numElems: Number of elements to swap");
    
    // byteSwap - with output buffer
    m.def("byteSwap",
          [](nb::capsule input, unsigned short elemSize, size_t numElems,
             nb::capsule output) {
              const void* inPtr = input.data();
              void* outPtr = output.data();
              sys::byteSwap(inPtr, elemSize, numElems, outPtr);
          },
          "buffer"_a, "elemSize"_a, "numElems"_a, "outputBuffer"_a,
          "Byte swap data from input to output buffer.\n\n"
          "Args:\n"
          "    buffer: Input memory buffer\n"
          "    elemSize: Size of each element in bytes\n"
          "    numElems: Number of elements to swap\n"
          "    outputBuffer: Output memory buffer");
    
    // alignedAlloc - with alignment parameter
    m.def("alignedAlloc",
          [](size_t size, size_t alignment) -> nb::capsule {
              void* ptr = sys::alignedAlloc(size, alignment);
              return nb::capsule(ptr, [](void* p) noexcept {
                  sys::alignedFree(p);
              });
          },
          "size"_a, "alignment"_a,
          "Allocate aligned memory.\n\n"
          "Args:\n"
          "    size: Number of bytes to allocate\n"
          "    alignment: Alignment boundary in bytes\n\n"
          "Returns:\n"
          "    Capsule: Memory buffer (automatically freed on destruction)");
    
    // alignedAlloc - default alignment
    m.def("alignedAlloc",
          [](size_t size) -> nb::capsule {
              void* ptr = sys::alignedAlloc(size);
              return nb::capsule(ptr, [](void* p) noexcept {
                  sys::alignedFree(p);
              });
          },
          "size"_a,
          "Allocate aligned memory with default alignment.\n\n"
          "Args:\n"
          "    size: Number of bytes to allocate\n\n"
          "Returns:\n"
          "    Capsule: Memory buffer (automatically freed on destruction)");
    
    // alignedFree
    m.def("alignedFree",
          [](nb::capsule p) {
              sys::alignedFree(p.data());
          },
          "p"_a,
          "Free aligned memory allocated with alignedAlloc.\n\n"
          "Args:\n"
          "    p: Memory buffer to free");
    
    // ========================================================================
    // UTCDateTime CLASS
    // ========================================================================
    
    nb::class_<sys::UTCDateTime>(m, "UTCDateTime",
        "Representation of a UTC date/time structure.\n\n"
        "Provides various constructors and methods for working with UTC timestamps.")
        
        // Constructors
        .def(nb::init<>(),
             "Construct with current UTC time")
        
        .def(nb::init<int, int, double>(),
             "hour"_a, "minute"_a, "second"_a,
             "Construct with time values (today's date).\n\n"
             "Args:\n"
             "    hour: Hour (0-23)\n"
             "    minute: Minute (0-59)\n"
             "    second: Second (0-59.999...)")
        
        .def(nb::init<int, int, int>(),
             "year"_a, "month"_a, "day"_a,
             "Construct with date values (time = 00:00:00).\n\n"
             "Args:\n"
             "    year: Year (e.g., 2024)\n"
             "    month: Month (1-12)\n"
             "    day: Day of month (1-31)")
        
        .def(nb::init<int, int, int, int, int, double>(),
             "year"_a, "month"_a, "day"_a, "hour"_a, "minute"_a, "second"_a,
             "Construct with date and time values.\n\n"
             "Args:\n"
             "    year: Year (e.g., 2024)\n"
             "    month: Month (1-12)\n"
             "    day: Day of month (1-31)\n"
             "    hour: Hour (0-23)\n"
             "    minute: Minute (0-59)\n"
             "    second: Second (0-59.999...)")
        
        .def(nb::init<double>(),
             "timeInMillis"_a,
             "Construct from milliseconds since epoch.\n\n"
             "Args:\n"
             "    timeInMillis: Milliseconds since January 1, 1970 00:00:00 UTC")
        
        .def(nb::init<const std::string&>(),
             "time"_a,
             "Construct from ISO8601 UTC string (YYYY-MM-DDTHH:MM:SSZ).\n\n"
             "Args:\n"
             "    time: ISO8601 formatted date/time string")
        
        .def(nb::init<const std::string&, const std::string&>(),
             "time"_a, "format"_a,
             "Construct from string with custom format.\n\n"
             "Args:\n"
             "    time: Date/time string\n"
             "    format: Format string (y=year, m=month, d=day, H=hour, M=minute, S=second)")
        
        // Methods
        .def("format",
             nb::overload_cast<>(&sys::UTCDateTime::format, nb::const_),
             "Format as ISO8601 UTC string.\n\n"
             "Returns:\n"
             "    str: Formatted string (YYYY-MM-DDTHH:MM:SSZ)")
        
        // Python special methods
        .def("__repr__",
             [](const sys::UTCDateTime& dt) {
                 return "<UTCDateTime: " + dt.format() + ">";
             },
             "Return string representation of UTCDateTime")
        
        .def("__str__",
             [](const sys::UTCDateTime& dt) {
                 return dt.format();
             },
             "Convert UTCDateTime to ISO8601 string");
    
    // Note: Stream operators (operator<< and operator>>) are intentionally 
    // omitted as they are not Pythonic. Use str() or .format() instead.
}
