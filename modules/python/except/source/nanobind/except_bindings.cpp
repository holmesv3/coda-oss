/*
 * =========================================================================
 * This file is part of except-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * except-python is free software; you can redistribute it and/or modify
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

#include "import/except.h"

namespace nb = nanobind;
using namespace except;

NB_MODULE(coda_except, m) {
    m.doc() = "CODA-OSS exception handling framework";
    
    // Context class - source location information
    nb::class_<Context>(m, "Context")
        .def(nb::init<const std::string&, int, const std::string&, 
                      const std::string&, const std::string&>(),
             nb::arg("file"), nb::arg("line"), nb::arg("func"),
             nb::arg("time") = "", nb::arg("message") = "")
        .def("getMessage", &Context::getMessage)
        .def("getTime", &Context::getTime)
        .def("getFunction", &Context::getFunction)
        .def("getFile", &Context::getFile)
        .def("getLine", &Context::getLine)
        .def_rw("mMessage", &Context::mMessage)
        .def_rw("mTime", &Context::mTime)
        .def_rw("mFunc", &Context::mFunc)
        .def_rw("mFile", &Context::mFile)
        .def_rw("mLine", &Context::mLine)
        .def("__str__", [](const Context& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        });
    
    // Trace class - exception trace
    nb::class_<Trace>(m, "Trace")
        .def(nb::init<>())
        .def("pushContext", &Trace::pushContext, nb::arg("context"))
        .def("getSize", &Trace::getSize)
        .def("__str__", [](const Trace& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        });
    
    // Throwable base class
    nb::class_<Throwable>(m, "Throwable")
        .def(nb::init<>())
        .def(nb::init<const std::string&>(), nb::arg("message"))
        .def(nb::init<const Context&>(), nb::arg("context"))
        .def("getMessage", &Throwable::getMessage)
        .def("getTrace", nb::overload_cast<>(&Throwable::getTrace), 
             nb::rv_policy::reference_internal)
        .def("getType", &Throwable::getType)
        .def("toString", nb::overload_cast<>(&Throwable::toString, nb::const_))
        .def("backtrace", &Throwable::backtrace, nb::rv_policy::reference)
        .def("getBacktrace", &Throwable::getBacktrace)
        .def("__str__", [](const Throwable& self) {
            return self.toString();
        });
    
    // Exception class (inherits from Throwable)
    nb::class_<Exception, Throwable>(m, "Exception")
        .def(nb::init<>())
        .def(nb::init<const std::string&>(), nb::arg("message"))
        .def(nb::init<const Context&>(), nb::arg("context"))
        .def(nb::init<const Throwable&, const Context&>(),
             nb::arg("throwable"), nb::arg("context"));
    
    // Register exception translator - converts C++ exceptions to Python
    nb::register_exception_translator([](const std::exception_ptr &p, void *) {
        try {
            std::rethrow_exception(p);
        } catch (const Exception &e) {
            PyErr_SetString(PyExc_RuntimeError, e.getMessage().c_str());
        } catch (const Throwable &e) {
            PyErr_SetString(PyExc_RuntimeError, e.getMessage().c_str());
        } catch (const std::exception &e) {
            PyErr_SetString(PyExc_RuntimeError, e.what());
        }
    });
}
