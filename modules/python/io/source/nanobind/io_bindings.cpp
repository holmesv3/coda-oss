/*
 * =========================================================================
 * This file is part of io-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * io-python is free software; you can redistribute it and/or modify
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

#include "import/io.h"

namespace nb = nanobind;
using namespace io;

NB_MODULE(coda_io, m) {
    m.doc() = "CODA-OSS I/O stream operations";
    
    // InputStream - abstract base class
    nb::class_<InputStream>(m, "InputStream")
        .def("read", [](InputStream& self, size_t size) {
            std::string buffer(size, '\0');
            sys::SSize_T bytesRead = self.read(&buffer[0], size);
            buffer.resize(bytesRead);
            return nb::bytes(buffer.data(), buffer.size());
        }, nb::arg("size"))
        .def("available", &InputStream::available);
    
    // OutputStream - abstract base class
    nb::class_<OutputStream>(m, "OutputStream")
        .def("write", [](OutputStream& self, const std::string& data) {
            self.write(data.data(), data.size());
        }, nb::arg("data"))
        .def("flush", &OutputStream::flush);
    
    // BidirectionalStream - combines input and output (single base for simplicity)
    nb::class_<BidirectionalStream, InputStream>(m, "BidirectionalStream")
        .def("write", [](BidirectionalStream& self, const std::string& data) {
            self.write(data.data(), data.size());
        }, nb::arg("data"))
        .def("flush", &BidirectionalStream::flush);
    
    // Seekable - interface for seekable streams
    nb::class_<Seekable>(m, "Seekable")
        .def("seek", &Seekable::seek, nb::arg("offset"), nb::arg("whence"))
        .def("tell", &Seekable::tell);
    
    // SeekableInputStream (just inherit from InputStream for simplicity)
    nb::class_<SeekableInputStream, InputStream>(m, "SeekableInputStream")
        .def("seek", &SeekableInputStream::seek, nb::arg("offset"), nb::arg("whence"))
        .def("tell", &SeekableInputStream::tell);
    
    // SeekableOutputStream (just inherit from OutputStream for simplicity)
    nb::class_<SeekableOutputStream, OutputStream>(m, "SeekableOutputStream")
        .def("seek", &SeekableOutputStream::seek, nb::arg("offset"), nb::arg("whence"))
        .def("tell", &SeekableOutputStream::tell);
    
    // StringStream - in-memory bidirectional stream
    nb::class_<StringStream, BidirectionalStream>(m, "StringStream")
        .def(nb::init<>())
        .def("str", [](const StringStream& self) {
            return self.stream().str();
        })
        .def("writeBytes", [](StringStream& self, nb::bytes bytes) {
            std::string_view sv(bytes.c_str(), bytes.size());
            self.write(sv.data(), sv.size());
        }, nb::arg("bytes"));
    
    // FileInputStreamOS
    nb::class_<FileInputStreamOS, SeekableInputStream>(m, "FileInputStream")
        .def(nb::init<const std::string&>(), nb::arg("filename"));
    
    // FileOutputStreamOS
    nb::class_<FileOutputStreamOS, SeekableOutputStream>(m, "FileOutputStream")
        .def(nb::init<const std::string&>(), nb::arg("filename"))
        .def(nb::init<const std::string&, int>(), nb::arg("filename"), nb::arg("creationFlags"));
}
