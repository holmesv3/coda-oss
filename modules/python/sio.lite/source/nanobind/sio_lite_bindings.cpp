/*
 * =========================================================================
 * This file is part of sio.lite-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * sio.lite-python is free software; you can redistribute it and/or modify
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
 */

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/ndarray.h>

#include "import/sio/lite.h"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(coda_sio_lite, m) {
    m.doc() = "CODA-OSS SIO lite I/O";
    
    // ========================================================================
    // FileHeader Class
    // ========================================================================
    auto fileHeader = nb::class_<sio::lite::FileHeader>(m, "FileHeader");
    
    // Element type constants as class attributes
    fileHeader.def_ro_static("UNSIGNED", &sio::lite::FileHeader::UNSIGNED);
    fileHeader.def_ro_static("SIGNED", &sio::lite::FileHeader::SIGNED);
    fileHeader.def_ro_static("FLOAT", &sio::lite::FileHeader::FLOAT);
    fileHeader.def_ro_static("COMPLEX_UNSIGNED", &sio::lite::FileHeader::COMPLEX_UNSIGNED);
    fileHeader.def_ro_static("COMPLEX_SIGNED", &sio::lite::FileHeader::COMPLEX_SIGNED);
    fileHeader.def_ro_static("COMPLEX_FLOAT", &sio::lite::FileHeader::COMPLEX_FLOAT);
    fileHeader.def_ro_static("N_BYTE_UNSIGNED", &sio::lite::FileHeader::N_BYTE_UNSIGNED);
    fileHeader.def_ro_static("N_BYTE_SIGNED", &sio::lite::FileHeader::N_BYTE_SIGNED);
    
    // Constructors
    fileHeader.def(nb::init<>());
    fileHeader.def(nb::init<size_t, size_t, size_t, int>(),
                   "numLines"_a, "numElements"_a, "elementSize"_a, "elementType"_a,
                   "Constructor\n\n"
                   "Args:\n"
                   "    numLines: Number of lines in the image\n"
                   "    numElements: Number of elements per line\n"
                   "    elementSize: Size of each element in bytes\n"
                   "    elementType: Element type constant");
    
    // Basic accessors
    fileHeader.def("getLength", &sio::lite::FileHeader::getLength,
                   "Returns the total header length");
    fileHeader.def("getNumLines", &sio::lite::FileHeader::getNumLines,
                   "Get the number of lines");
    fileHeader.def("setNumLines", &sio::lite::FileHeader::setNumLines, "numLines"_a,
                   "Set the number of lines");
    fileHeader.def("getNumElements", &sio::lite::FileHeader::getNumElements,
                   "Get the number of elements per line");
    fileHeader.def("setNumElements", &sio::lite::FileHeader::setNumElements, "numElements"_a,
                   "Set the number of elements per line");
    fileHeader.def("getElementSize", &sio::lite::FileHeader::getElementSize,
                   "Get the element size in bytes");
    fileHeader.def("setElementSize", &sio::lite::FileHeader::setElementSize, "elementSize"_a,
                   "Set the element size in bytes");
    fileHeader.def("getElementType", &sio::lite::FileHeader::getElementType,
                   "Get the element type");
    fileHeader.def("setElementType", &sio::lite::FileHeader::setElementType, "elementType"_a,
                   "Set the element type");
    fileHeader.def("getElementTypeAsString", &sio::lite::FileHeader::getElementTypeAsString,
                   "Get string representation of element type");
    
    // Version methods
    fileHeader.def("getVersion", &sio::lite::FileHeader::getVersion,
                   "Get SIO file version");
    fileHeader.def("setVersion", &sio::lite::FileHeader::setVersion, "version"_a,
                   "Set SIO file version");
    
    // Endianness
    fileHeader.def("isDifferentByteOrdering", &sio::lite::FileHeader::isDifferentByteOrdering,
                   "Check if byte ordering differs from system");
    
    // User data methods
    fileHeader.def("userDataFieldExists", &sio::lite::FileHeader::userDataFieldExists, "key"_a,
                   "Check if user data key exists");
    fileHeader.def("getUserData",
                   static_cast<std::vector<sys::byte>& (sio::lite::FileHeader::*)(const std::string&)>(&sio::lite::FileHeader::getUserData),
                   "key"_a,
                   nb::rv_policy::reference_internal,
                   "Get user data value by key");
    fileHeader.def("addUserData",
                   [](sio::lite::FileHeader& self, const std::string& key, const std::string& value) {
                       self.addUserData(key, value);
                   },
                   "key"_a, "value"_a,
                   "Add user data string");
    fileHeader.def("addUserData",
                   [](sio::lite::FileHeader& self, const std::string& key, int value) {
                       self.addUserData(key, value);
                   },
                   "key"_a, "value"_a,
                   "Add user data integer");
    
    // ========================================================================
    // FileWriter Class
    // ========================================================================
    nb::class_<sio::lite::FileWriter>(m, "FileWriter")
        .def(nb::init<const std::string&>(), "outputFile"_a,
             "Constructor taking output filename")
        .def(nb::init<io::OutputStream*, bool>(), "stream"_a, "adopt"_a = true,
             "Constructor taking output stream")
        
        // Classic write method - accepts raw pointer (for __array_interface__ compatibility)
        .def("write",
             [](sio::lite::FileWriter& self,
                sio::lite::FileHeader* header,
                uintptr_t dataPointer) {
                 const void* buffer = reinterpret_cast<const void*>(dataPointer);
                 self.write(header, buffer);
             },
             "header"_a, "data"_a,
             "Write SIO file from header and data pointer\n\n"
             "Args:\n"
             "    header: FileHeader with metadata\n"
             "    data: Raw pointer to data buffer")
        
        // Modern API - accept NumPy array directly
        .def("writeArray",
             [](sio::lite::FileWriter& self,
                sio::lite::FileHeader* header,
                nb::ndarray<nb::c_contig> array) {
                 void* ptr = array.data();
                 self.write(header, ptr);
             },
             "header"_a, "array"_a,
             "Write SIO file from header and NumPy array\n\n"
             "Args:\n"
             "    header: FileHeader with metadata\n"
             "    array: NumPy array (must be C-contiguous)")
        
        // Alternative write with explicit parameters
        .def("write",
             [](sio::lite::FileWriter& self,
                int numLines, int numElements, int elementSize,
                int elementType, uintptr_t dataPointer, int numBands) {
                 const void* buffer = reinterpret_cast<const void*>(dataPointer);
                 self.write(numLines, numElements, elementSize, elementType, buffer, numBands);
             },
             "numLines"_a, "numElements"_a, "elementSize"_a,
             "elementType"_a, "data"_a, "numBands"_a = 1,
             "Write SIO file with explicit parameters");
    
    // ========================================================================
    // StreamReader Class
    // ========================================================================
    nb::class_<sio::lite::StreamReader, io::InputStream>(m, "StreamReader")
        .def(nb::init<>(),
             "Default constructor")
        .def(nb::init<io::InputStream*, bool>(), "is"_a, "adopt"_a = false,
             "Constructor taking input stream")
        
        .def("setInputStream", &sio::lite::StreamReader::setInputStream,
             "is"_a, "adopt"_a = false,
             "Set input stream")
        .def("getInputStream", &sio::lite::StreamReader::getInputStream,
             nb::rv_policy::reference_internal,
             "Get underlying input stream")
        .def("getHeader",
             static_cast<sio::lite::FileHeader* (sio::lite::StreamReader::*)()>(&sio::lite::StreamReader::getHeader),
             nb::rv_policy::reference_internal,
             "Get file header")
        
        // Classic read method - accepts raw pointer (for __array_interface__ compatibility)
        .def("read",
             [](sio::lite::StreamReader& self, uintptr_t dataPointer, size_t size) {
                 sys::byte* buffer = reinterpret_cast<sys::byte*>(dataPointer);
                 return self.read(buffer, size);
             },
             "data"_a, "size"_a,
             "Read data into buffer\n\n"
             "Args:\n"
             "    data: Raw pointer to buffer\n"
             "    size: Number of bytes to read\n\n"
             "Returns:\n"
             "    Number of bytes actually read")
        
        // Modern API - read into NumPy array directly
        .def("readArray",
             [](sio::lite::StreamReader& self, nb::ndarray<nb::c_contig> array) {
                 void* ptr = array.data();
                 size_t size = array.size() * array.itemsize();
                 return self.read(static_cast<sys::byte*>(ptr), size);
             },
             "array"_a,
             "Read data into NumPy array\n\n"
             "Args:\n"
             "    array: NumPy array to read into (must be C-contiguous)\n\n"
             "Returns:\n"
             "    Number of bytes actually read")
        
        .def("available", &sio::lite::StreamReader::available,
             "Get number of bytes available");
    
    // ========================================================================
    // FileReader Class
    // ========================================================================
    nb::class_<sio::lite::FileReader, sio::lite::StreamReader>(m, "FileReader")
        .def(nb::init<>(),
             "Default constructor")
        .def(nb::init<const std::string&>(), "file"_a,
             "Constructor taking filename")
        .def(nb::init<io::FileInputStream*, bool>(), "is"_a, "adopt"_a = false,
             "Constructor taking file input stream")
        
        // Seekable interface
        .def("seek", &sio::lite::FileReader::seek, "offset"_a, "whence"_a,
             "Seek within file (position relative to header)\n\n"
             "Args:\n"
             "    offset: Byte offset\n"
             "    whence: Seek mode (Seekable.START, CURRENT, or END)")
        .def("tell", &sio::lite::FileReader::tell,
             "Get current position (relative to header)\n\n"
             "Returns:\n"
             "    Current byte position");
}
