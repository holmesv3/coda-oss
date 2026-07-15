/*
 * =========================================================================
 * This file is part of math.linear-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * math.linear-python is free software; you can redistribute it and/or modify
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

#include "math/linear/VectorN.h"
#include "math/linear/Vector.h"
#include "math/linear/MatrixMxN.h"
#include "math/linear/Matrix2D.h"

namespace nb = nanobind;
using namespace nb::literals;

// Make STL vectors opaque to avoid type caster conflicts
NB_MAKE_OPAQUE(std::vector<double>)
NB_MAKE_OPAQUE(std::vector<std::vector<double>>)

// Helper template for binding fixed-size MatrixMxN types
template<size_t M, size_t N>
void bindMatrixMxN(nb::module_& m, const char* name) {
    using MatrixType = math::linear::MatrixMxN<M, N, double>;
    
    nb::class_<MatrixType>(m, name)
        .def(nb::init<>())
        .def("rows", &MatrixType::rows)
        .def("cols", &MatrixType::cols)
        .def("__getitem__", [](const MatrixType& self, nb::tuple idx) {
            if (idx.size() != 2) {
                throw nb::type_error("Expected a tuple of the form (size_t, size_t)");
            }
            ssize_t m = nb::cast<ssize_t>(idx[0]);
            ssize_t n = nb::cast<ssize_t>(idx[1]);
            if (m < 0 || m >= static_cast<ssize_t>(self.rows()) ||
                n < 0 || n >= static_cast<ssize_t>(self.cols())) {
                throw nb::index_error("Index out of range");
            }
            return self(m, n);
        })
        .def("__setitem__", [](MatrixType& self, nb::tuple idx, double val) {
            if (idx.size() != 2) {
                throw nb::type_error("Expected a tuple of the form (size_t, size_t)");
            }
            ssize_t m = nb::cast<ssize_t>(idx[0]);
            ssize_t n = nb::cast<ssize_t>(idx[1]);
            if (m < 0 || m >= static_cast<ssize_t>(self.rows()) ||
                n < 0 || n >= static_cast<ssize_t>(self.cols())) {
                throw nb::index_error("Index out of range");
            }
            self(m, n) = val;
        })
        .def("__str__", [](const MatrixType& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("vals", [](const MatrixType& self) {
            std::vector<std::vector<double>> result(self.rows());
            for (size_t i = 0; i < self.rows(); ++i) {
                result[i] = std::vector<double>(self.cols());
                for (size_t j = 0; j < self.cols(); ++j) {
                    result[i][j] = self(i, j);
                }
            }
            return result;
        });
}

NB_MODULE(coda_math_linear, m) {
    m.doc() = "CODA-OSS linear algebra module";
    
    // ========================================================================
    // Helper vector types
    // ========================================================================
    nb::bind_vector<std::vector<double>>(m, "std_vector_double");
    nb::bind_vector<std::vector<std::vector<double>>>(m, "std_vector_vector_double");
    
    // ========================================================================
    // Vector2 - Fixed-size 2D vector
    // ========================================================================
    nb::class_<math::linear::VectorN<2, double>>(m, "Vector2")
        .def(nb::init<>())
        .def(nb::init<const std::vector<double>&>())
        .def("__getitem__", [](const math::linear::VectorN<2, double>& self, ssize_t i) {
            if (i < 0 || i >= 2) {
                throw nb::index_error("Index out of range");
            }
            return self[i];
        })
        .def("__setitem__", [](math::linear::VectorN<2, double>& self, ssize_t i, double val) {
            if (i < 0 || i >= 2) {
                throw nb::index_error("Index out of range");
            }
            self[i] = val;
        })
        .def("__str__", [](const math::linear::VectorN<2, double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("__deepcopy__", [](const math::linear::VectorN<2, double>& self, nb::dict) {
            return math::linear::VectorN<2, double>(self);
        })
        .def("vals", [](const math::linear::VectorN<2, double>& self) {
            return self.matrix().col(0);
        })
        // Pickle support
        .def("__getstate__", [](const math::linear::VectorN<2, double>& self) {
            return nb::make_tuple(self.matrix().col(0));
        })
        .def("__setstate__", [](math::linear::VectorN<2, double>& self, nb::tuple t) {
            auto vec = nb::cast<std::vector<double>>(t[0]);
            new (&self) math::linear::VectorN<2, double>(vec);
        });
    
    // ========================================================================
    // Vector3 - Fixed-size 3D vector
    // ========================================================================
    nb::class_<math::linear::VectorN<3, double>>(m, "Vector3")
        .def(nb::init<>())
        .def(nb::init<const std::vector<double>&>())
        .def("__getitem__", [](const math::linear::VectorN<3, double>& self, ssize_t i) {
            if (i < 0 || i >= 3) {
                throw nb::index_error("Index out of range");
            }
            return self[i];
        })
        .def("__setitem__", [](math::linear::VectorN<3, double>& self, ssize_t i, double val) {
            if (i < 0 || i >= 3) {
                throw nb::index_error("Index out of range");
            }
            self[i] = val;
        })
        .def("__str__", [](const math::linear::VectorN<3, double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("__deepcopy__", [](const math::linear::VectorN<3, double>& self, nb::dict) {
            return math::linear::VectorN<3, double>(self);
        })
        .def("vals", [](const math::linear::VectorN<3, double>& self) {
            return self.matrix().col(0);
        })
        // Pickle support
        .def("__getstate__", [](const math::linear::VectorN<3, double>& self) {
            return nb::make_tuple(self.matrix().col(0));
        })
        .def("__setstate__", [](math::linear::VectorN<3, double>& self, nb::tuple t) {
            auto vec = nb::cast<std::vector<double>>(t[0]);
            new (&self) math::linear::VectorN<3, double>(vec);
        });
    
    // ========================================================================
    // VectorDouble - Dynamic-size vector
    // ========================================================================
    nb::class_<math::linear::Vector<double>>(m, "VectorDouble")
        .def(nb::init<size_t>())
        .def(nb::init<const std::vector<double>&>())
        .def("size", &math::linear::Vector<double>::size)
        .def("__getitem__", [](const math::linear::Vector<double>& self, ssize_t i) {
            if (i < 0 || i >= static_cast<ssize_t>(self.size())) {
                throw nb::index_error("Index out of range");
            }
            return self[i];
        })
        .def("__setitem__", [](math::linear::Vector<double>& self, ssize_t i, double val) {
            if (i < 0 || i >= static_cast<ssize_t>(self.size())) {
                throw nb::index_error("Index out of range");
            }
            self[i] = val;
        })
        .def("__str__", [](const math::linear::Vector<double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("vals", [](const math::linear::Vector<double>& self) {
            return self.matrix().col(0);
        });
    
    // ========================================================================
    // MatrixDouble - Dynamic-size 2D matrix
    // ========================================================================
    nb::class_<math::linear::Matrix2D<double>>(m, "MatrixDouble")
        .def(nb::init<size_t, size_t>())
        .def("rows", &math::linear::Matrix2D<double>::rows)
        .def("cols", &math::linear::Matrix2D<double>::cols)
        .def("__getitem__", [](const math::linear::Matrix2D<double>& self, nb::tuple idx) {
            if (idx.size() != 2) {
                throw nb::type_error("Expected a tuple of the form (size_t, size_t)");
            }
            ssize_t m = nb::cast<ssize_t>(idx[0]);
            ssize_t n = nb::cast<ssize_t>(idx[1]);
            if (m < 0 || m >= static_cast<ssize_t>(self.rows()) ||
                n < 0 || n >= static_cast<ssize_t>(self.cols())) {
                throw nb::index_error("Index out of range");
            }
            return self(m, n);
        })
        .def("__setitem__", [](math::linear::Matrix2D<double>& self, nb::tuple idx, double val) {
            if (idx.size() != 2) {
                throw nb::type_error("Expected a tuple of the form (size_t, size_t)");
            }
            ssize_t m = nb::cast<ssize_t>(idx[0]);
            ssize_t n = nb::cast<ssize_t>(idx[1]);
            if (m < 0 || m >= static_cast<ssize_t>(self.rows()) ||
                n < 0 || n >= static_cast<ssize_t>(self.cols())) {
                throw nb::index_error("Index out of range");
            }
            self(m, n) = val;
        })
        .def("__str__", [](const math::linear::Matrix2D<double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("vals", [](const math::linear::Matrix2D<double>& self) {
            std::vector<std::vector<double>> result(self.rows());
            for (size_t i = 0; i < self.rows(); ++i) {
                result[i] = std::vector<double>(self.cols());
                for (size_t j = 0; j < self.cols(); ++j) {
                    result[i][j] = self(i, j);
                }
            }
            return result;
        });
    
    // ========================================================================
    // Fixed-size matrices (14 instantiations)
    // ========================================================================
    bindMatrixMxN<1, 1>(m, "Matrix1x1");
    bindMatrixMxN<1, 2>(m, "Matrix1x2");
    bindMatrixMxN<1, 3>(m, "Matrix1x3");
    bindMatrixMxN<2, 1>(m, "Matrix2x1");
    bindMatrixMxN<2, 2>(m, "Matrix2x2");
    bindMatrixMxN<2, 3>(m, "Matrix2x3");
    bindMatrixMxN<2, 7>(m, "Matrix2x7");
    bindMatrixMxN<3, 1>(m, "Matrix3x1");
    bindMatrixMxN<3, 2>(m, "Matrix3x2");
    bindMatrixMxN<3, 3>(m, "Matrix3x3");
    bindMatrixMxN<3, 7>(m, "Matrix3x7");
    bindMatrixMxN<7, 2>(m, "Matrix7x2");
    bindMatrixMxN<7, 3>(m, "Matrix7x3");
    bindMatrixMxN<7, 7>(m, "Matrix7x7");
    
    // ========================================================================
    // cross product function
    // ========================================================================
    m.def("cross", 
          static_cast<math::linear::VectorN<3, double> (*)(const math::linear::VectorN<3, double>&, const math::linear::VectorN<3, double>&)>(&math::linear::cross<double>),
          "a"_a, "b"_a,
          "Compute cross product of two Vector3 objects");
}
