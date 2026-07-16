/*
 * =========================================================================
 * This file is part of coda_types-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * coda_types-python is free software; you can redistribute it and/or modify
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
#include <nanobind/stl/bind_vector.h>

#include "sys/Conf.h"
#include "types/RowCol.h"
#include "types/RgAz.h"

// Make these vector types opaque so we can use bind_vector
NB_MAKE_OPAQUE(std::vector<types::RowCol<sys::SSize_T>>);
NB_MAKE_OPAQUE(std::vector<types::RowCol<double>>);
NB_MAKE_OPAQUE(std::vector<size_t>);
NB_MAKE_OPAQUE(std::vector<std::string>);

namespace nb = nanobind;
using namespace nb::literals;

// Helper template to bind RowCol<T>
template<typename T>
void bindRowCol(nb::module_& m, const char* name) {
    nb::class_<types::RowCol<T>>(m, name)
        .def(nb::init<>())
        .def(nb::init<T, T>(), "row"_a, "col"_a)
        .def_rw("row", &types::RowCol<T>::row)
        .def_rw("col", &types::RowCol<T>::col)
        // Arithmetic operators with RowCol
        .def(nb::self + nb::self)
        .def(nb::self - nb::self)
        .def(nb::self * nb::self)
        .def(nb::self / nb::self)
        .def(nb::self += nb::self)
        .def(nb::self -= nb::self)
        .def(nb::self *= nb::self)
        .def(nb::self /= nb::self)
        // Arithmetic operators with scalar
        .def(nb::self + T())
        .def(nb::self - T())
        .def(nb::self * T())
        .def(nb::self / T())
        .def(nb::self += T())
        .def(nb::self -= T())
        .def(nb::self *= T())
        .def(nb::self /= T())
        // Comparison operators
        .def(nb::self == nb::self)
        .def(nb::self != nb::self)
        // Pickle support
        .def("__getstate__", [](const types::RowCol<T>& self) {
            return nb::make_tuple(self.row, self.col);
        })
        .def("__setstate__", [](types::RowCol<T>& self, nb::tuple t) {
            self.row = nb::cast<T>(t[0]);
            self.col = nb::cast<T>(t[1]);
        })
        // String representation
        .def("__repr__", [name](const types::RowCol<T>& self) {
            return std::string(name) + "(row=" + std::to_string(self.row) + 
                   ", col=" + std::to_string(self.col) + ")";
        });
}

// Helper template to bind RgAz<T>
template<typename T>
void bindRgAz(nb::module_& m, const char* name) {
    nb::class_<types::RgAz<T>>(m, name)
        .def(nb::init<>())
        .def(nb::init<T, T>(), "rg"_a, "az"_a)
        .def_rw("rg", &types::RgAz<T>::rg)
        .def_rw("az", &types::RgAz<T>::az)
        // Arithmetic operators with RgAz
        .def(nb::self + nb::self)
        .def(nb::self - nb::self)
        .def(nb::self * nb::self)
        .def(nb::self / nb::self)
        .def(nb::self += nb::self)
        .def(nb::self -= nb::self)
        .def(nb::self *= nb::self)
        .def(nb::self /= nb::self)
        // Arithmetic operators with scalar
        .def(nb::self + T())
        .def(nb::self - T())
        .def(nb::self * T())
        .def(nb::self / T())
        .def(nb::self += T())
        .def(nb::self -= T())
        .def(nb::self *= T())
        .def(nb::self /= T())
        // Comparison operators
        .def(nb::self == nb::self)
        .def(nb::self != nb::self)
        // Pickle support
        .def("__getstate__", [](const types::RgAz<T>& self) {
            return nb::make_tuple(self.rg, self.az);
        })
        .def("__setstate__", [](types::RgAz<T>& self, nb::tuple t) {
            self.rg = nb::cast<T>(t[0]);
            self.az = nb::cast<T>(t[1]);
        })
        // String representation
        .def("__repr__", [name](const types::RgAz<T>& self) {
            return std::string(name) + "(rg=" + std::to_string(self.rg) + 
                   ", az=" + std::to_string(self.az) + ")";
        });
}

NB_MODULE(coda_types, m) {
    m.doc() = "CODA-OSS types module - RowCol and RgAz types";
    
    // Bind RowCol template instantiations
    bindRowCol<double>(m, "RowColDouble");
    bindRowCol<sys::SSize_T>(m, "RowColInt");
    bindRowCol<size_t>(m, "RowColSizeT");
    
    // Bind RgAz template instantiations
    bindRgAz<double>(m, "RgAzDouble");
    
    // Bind vector types with pickle support
    // For vectors of RowCol
    nb::bind_vector<std::vector<types::RowCol<sys::SSize_T>>>(m, "VectorRowColInt")
        .def("__getstate__", [](const std::vector<types::RowCol<sys::SSize_T>>& self) {
            nb::list items;
            for (const auto& elem : self) {
                items.append(nb::make_tuple(elem.row, elem.col));
            }
            return nb::make_tuple(nb::int_(-1), items);
        })
        .def("__setstate__", [](std::vector<types::RowCol<sys::SSize_T>>& self, nb::tuple t) {
            nb::list items = nb::cast<nb::list>(t[1]);
            std::vector<types::RowCol<sys::SSize_T>> temp;
            temp.reserve(nb::len(items));
            for (size_t i = 0; i < nb::len(items); ++i) {
                nb::tuple elem = nb::cast<nb::tuple>(items[i]);
                temp.emplace_back(
                    nb::cast<sys::SSize_T>(elem[0]),  // row
                    nb::cast<sys::SSize_T>(elem[1])   // col
                );
            }
            new (&self) std::vector<types::RowCol<sys::SSize_T>>(std::move(temp));
        });
    
    nb::bind_vector<std::vector<types::RowCol<double>>>(m, "VectorRowColDouble")
        .def("__getstate__", [](const std::vector<types::RowCol<double>>& self) {
            nb::list items;
            for (const auto& elem : self) {
                items.append(nb::make_tuple(elem.row, elem.col));
            }
            return nb::make_tuple(nb::int_(-1), items);
        })
        .def("__setstate__", [](std::vector<types::RowCol<double>>& self, nb::tuple t) {
            nb::list items = nb::cast<nb::list>(t[1]);
            std::vector<types::RowCol<double>> temp;
            temp.reserve(nb::len(items));
            for (size_t i = 0; i < nb::len(items); ++i) {
                nb::tuple elem = nb::cast<nb::tuple>(items[i]);
                temp.emplace_back(
                    nb::cast<double>(elem[0]),  // row
                    nb::cast<double>(elem[1])   // col
                );
            }
            new (&self) std::vector<types::RowCol<double>>(std::move(temp));
        });
    
    // For basic types
    nb::bind_vector<std::vector<size_t>>(m, "VectorSizeT")
        .def("__getstate__", [](const std::vector<size_t>& self) {
            nb::list items;
            for (const auto& elem : self) {
                items.append(elem);
            }
            return nb::make_tuple(nb::int_(-1), items);
        })
        .def("__setstate__", [](std::vector<size_t>& self, nb::tuple t) {
            nb::list items = nb::cast<nb::list>(t[1]);
            std::vector<size_t> temp;
            temp.reserve(nb::len(items));
            for (size_t i = 0; i < nb::len(items); ++i) {
                temp.push_back(nb::cast<size_t>(items[i]));
            }
            new (&self) std::vector<size_t>(std::move(temp));
        });
    
    nb::bind_vector<std::vector<std::string>>(m, "VectorString")
        .def("__getstate__", [](const std::vector<std::string>& self) {
            nb::list items;
            for (const auto& elem : self) {
                items.append(elem);
            }
            return nb::make_tuple(nb::int_(-1), items);
        })
        .def("__setstate__", [](std::vector<std::string>& self, nb::tuple t) {
            nb::list items = nb::cast<nb::list>(t[1]);
            std::vector<std::string> temp;
            temp.reserve(nb::len(items));
            for (size_t i = 0; i < nb::len(items); ++i) {
                temp.push_back(nb::cast<std::string>(items[i]));
            }
            new (&self) std::vector<std::string>(std::move(temp));
        });
}
