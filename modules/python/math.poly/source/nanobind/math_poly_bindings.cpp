/*
 * =========================================================================
 * This file is part of math.poly-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * math.poly-python is free software; you can redistribute it and/or modify
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
#include <nanobind/ndarray.h>

#include "import/math/linear.h"
#include "math/poly/OneD.h"
#include "math/poly/TwoD.h"
#include "math/poly/Fit.h"

namespace nb = nanobind;
using namespace nb::literals;

using Vector3 = math::linear::VectorN<3, double>;
using VectorDouble = math::linear::Vector<double>;
using MatrixDouble = math::linear::Matrix2D<double>;

// Make STL vectors opaque to avoid type caster conflicts
NB_MAKE_OPAQUE(std::vector<double>)
NB_MAKE_OPAQUE(std::vector<Vector3>)
NB_MAKE_OPAQUE(std::vector<math::poly::OneD<double>>)

NB_MODULE(coda_math_poly, m) {
    m.doc() = "CODA-OSS polynomial module";
    
    // ========================================================================
    // Helper vector types
    // ========================================================================
    nb::bind_vector<std::vector<double>>(m, "StdVectorDouble");
    nb::bind_vector<std::vector<Vector3>>(m, "Vector3Coefficients");
    
    // ========================================================================
    // Poly1D - 1D polynomial with double coefficients
    // ========================================================================
    auto poly1d = nb::class_<math::poly::OneD<double>>(m, "Poly1D");
    
    poly1d.def(nb::init<>())
        .def(nb::init<size_t>(), "order"_a)
        .def(nb::init<const std::vector<double>&>(), "coeffs"_a)
        .def("order", &math::poly::OneD<double>::order)
        .def("size", &math::poly::OneD<double>::size)
        .def("empty", &math::poly::OneD<double>::empty)
        .def("coeffs", 
             static_cast<const std::vector<double>& (math::poly::OneD<double>::*)() const>(&math::poly::OneD<double>::coeffs),
             nb::rv_policy::reference_internal)
        
        // Element access with bounds checking
        .def("__getitem__", [](const math::poly::OneD<double>& self, ssize_t i) {
            if (i > static_cast<ssize_t>(self.order())) {
                throw nb::index_error("Index out of range");
            }
            return self[i];
        })
        .def("__setitem__", [](math::poly::OneD<double>& self, ssize_t i, double val) {
            if (i > static_cast<ssize_t>(self.order())) {
                throw nb::index_error("Index out of range");
            }
            self[i] = val;
        })
        
        // String representation
        .def("__str__", [](const math::poly::OneD<double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        
        // Deep copy
        .def("__deepcopy__", [](const math::poly::OneD<double>& self, nb::dict) {
            return math::poly::OneD<double>(self);
        })
        
        // Callable - batch evaluation with Python sequences
        .def("__call__", [](const math::poly::OneD<double>& self, nb::object input) {
            // Single value
            try {
                double x = nb::cast<double>(input);
                return nb::cast(self(x));
            } catch (...) {}
            
            // Sequence of values
            if (!nb::isinstance<nb::sequence>(input)) {
                throw nb::type_error("Expecting a number or sequence");
            }
            nb::list result;
            for (auto item : nb::cast<nb::list>(input)) {
                double x = nb::cast<double>(item);
                result.append(self(x));
            }
            return nb::cast(result);
        })
        
        // NumPy array conversion using nanobind ndarray
        .def("asArray", [](const math::poly::OneD<double>& self) {
            if (self.empty()) {
                return nb::ndarray<nb::numpy, double>(nullptr, {0});
            }
            size_t size = self.size();
            double* data = new double[size];
            for (size_t i = 0; i < size; ++i) {
                data[i] = self[i];
            }
            nb::capsule owner(data, [](void* p) noexcept {
                delete[] static_cast<double*>(p);
            });
            return nb::ndarray<nb::numpy, double>(data, {size}, owner);
        })
        
        // Pickle support
        .def("__getstate__", [](const math::poly::OneD<double>& self) {
            return nb::make_tuple(self.coeffs());
        })
        .def("__setstate__", [](math::poly::OneD<double>& self, nb::tuple t) {
            auto coeffs = nb::cast<std::vector<double>>(t[0]);
            new (&self) math::poly::OneD<double>(coeffs);
        });
    
    // Static method fromArray (defined in Python-like way)
    poly1d.def_static("fromArray", [](nb::ndarray<nb::numpy, double> array) {
        if (array.size() == 0) {
            return math::poly::OneD<double>();
        }
        std::vector<double> coeffs(array.size());
        for (size_t i = 0; i < array.size(); ++i) {
            coeffs[i] = array.data()[i];
        }
        return math::poly::OneD<double>(coeffs);
    }, "array"_a);
    
    // ========================================================================
    // Poly2D - 2D polynomial with double coefficients
    // ========================================================================
    auto poly2d = nb::class_<math::poly::TwoD<double>>(m, "Poly2D");
    
    poly2d.def(nb::init<>())
        .def(nb::init<size_t, size_t>(), "orderX"_a, "orderY"_a)
        .def("orderX", &math::poly::TwoD<double>::orderX)
        .def("orderY", &math::poly::TwoD<double>::orderY)
        .def("empty", &math::poly::TwoD<double>::empty)
        .def("coeffs", 
             static_cast<const std::vector<math::poly::OneD<double>>& (math::poly::TwoD<double>::*)() const>(&math::poly::TwoD<double>::coeffs),
             nb::rv_policy::reference_internal)
        
        // 2D element access with tuple indexing
        .def("__getitem__", [](const math::poly::TwoD<double>& self, nb::tuple idx) {
            if (idx.size() != 2) {
                throw nb::type_error("Expecting a tuple (xpow, ypow)");
            }
            ssize_t xpow = nb::cast<ssize_t>(idx[0]);
            ssize_t ypow = nb::cast<ssize_t>(idx[1]);
            if (xpow > static_cast<ssize_t>(self.orderX()) || 
                ypow > static_cast<ssize_t>(self.orderY())) {
                throw nb::index_error("Index out of range");
            }
            return self[xpow][ypow];
        })
        .def("__setitem__", [](math::poly::TwoD<double>& self, nb::tuple idx, double val) {
            if (idx.size() != 2) {
                throw nb::type_error("Expecting a tuple (xpow, ypow)");
            }
            ssize_t xpow = nb::cast<ssize_t>(idx[0]);
            ssize_t ypow = nb::cast<ssize_t>(idx[1]);
            if (xpow > static_cast<ssize_t>(self.orderX()) || 
                ypow > static_cast<ssize_t>(self.orderY())) {
                throw nb::index_error("Index out of range");
            }
            self[xpow][ypow] = val;
        })
        
        // String representation
        .def("__str__", [](const math::poly::TwoD<double>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        
        // Deep copy
        .def("__deepcopy__", [](const math::poly::TwoD<double>& self, nb::dict) {
            return math::poly::TwoD<double>(self);
        })
        
        // Callable - batch evaluation with two Python sequences
        .def("__call__", [](const math::poly::TwoD<double>& self, 
                            nb::object x_input, nb::object y_input) {
            if (!nb::isinstance<nb::sequence>(x_input) || 
                !nb::isinstance<nb::sequence>(y_input)) {
                throw nb::type_error("Expecting sequences");
            }
            nb::list x_list = nb::cast<nb::list>(x_input);
            nb::list y_list = nb::cast<nb::list>(y_input);
            
            if (x_list.size() != y_list.size()) {
                throw nb::value_error("Input sequences must have same length");
            }
            
            nb::list result;
            for (size_t i = 0; i < x_list.size(); ++i) {
                double x = nb::cast<double>(x_list[i]);
                double y = nb::cast<double>(y_list[i]);
                result.append(self(x, y));
            }
            return result;
        })
        
        // NumPy array conversion
        .def("asArray", [](const math::poly::TwoD<double>& self) {
            if (self.empty()) {
                return nb::ndarray<nb::numpy, double>(nullptr, {0, 0});
            }
            size_t rows = self.orderX() + 1;
            size_t cols = self.orderY() + 1;
            double* data = new double[rows * cols];
            
            for (size_t i = 0; i < rows; ++i) {
                for (size_t j = 0; j < cols; ++j) {
                    data[i * cols + j] = self[i][j];
                }
            }
            
            nb::capsule owner(data, [](void* p) noexcept {
                delete[] static_cast<double*>(p);
            });
            return nb::ndarray<nb::numpy, double>(data, {rows, cols}, owner);
        })
        
        // Pickle support
        .def("__getstate__", [](const math::poly::TwoD<double>& self) {
            return nb::make_tuple(self.coeffs());
        })
        .def("__setstate__", [](math::poly::TwoD<double>& self, nb::tuple t) {
            auto coeffs = nb::cast<std::vector<math::poly::OneD<double>>>(t[0]);
            if (coeffs.empty()) {
                new (&self) math::poly::TwoD<double>();
            } else {
                new (&self) math::poly::TwoD<double>(coeffs.size() - 1, coeffs[0].order());
                for (size_t i = 0; i < coeffs.size(); ++i) {
                    for (size_t j = 0; j <= coeffs[i].order(); ++j) {
                        self[i][j] = coeffs[i][j];
                    }
                }
            }
        });
    
    // Static method fromArray
    poly2d.def_static("fromArray", [](nb::ndarray<nb::numpy, double> array) {
        if (array.ndim() != 2 || array.shape(0) == 0) {
            return math::poly::TwoD<double>();
        }
        size_t rows = array.shape(0);
        size_t cols = array.shape(1);
        math::poly::TwoD<double> result(rows - 1, cols - 1);
        
        for (size_t i = 0; i < rows; ++i) {
            for (size_t j = 0; j < cols; ++j) {
                result[i][j] = array.data()[i * cols + j];
            }
        }
        return result;
    }, "array"_a);
    
    // Helper for Poly1D vectors
    nb::bind_vector<std::vector<math::poly::OneD<double>>>(m, "Poly1DVector");
    
    // ========================================================================
    // PolyVector3 - 1D polynomial with Vector3 coefficients
    // ========================================================================
    nb::class_<math::poly::OneD<Vector3>>(m, "PolyVector3")
        .def(nb::init<>())
        .def(nb::init<size_t>(), "order"_a)
        .def("order", &math::poly::OneD<Vector3>::order)
        .def("size", &math::poly::OneD<Vector3>::size)
        .def("__getitem__", [](const math::poly::OneD<Vector3>& self, ssize_t i) {
            return self[i];
        })
        .def("__setitem__", [](math::poly::OneD<Vector3>& self, ssize_t i, const Vector3& val) {
            self[i] = val;
        })
        .def("__str__", [](const math::poly::OneD<Vector3>& self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        })
        .def("__deepcopy__", [](const math::poly::OneD<Vector3>& self, nb::dict) {
            return math::poly::OneD<Vector3>(self);
        })
        // Callable for PolyVector3
        .def("__call__", [](const math::poly::OneD<Vector3>& self, nb::object input) {
            if (!nb::isinstance<nb::sequence>(input)) {
                throw nb::type_error("Expecting a sequence");
            }
            nb::list result;
            for (auto item : nb::cast<nb::list>(input)) {
                double x = nb::cast<double>(item);
                Vector3 val = self(x);
                // Return Vector3 object
                result.append(val);
            }
            return result;
        });
    
    // ========================================================================
    // Polynomial fitting functions
    // ========================================================================
    
    // 1D fit from std::vector
    m.def("fit", [](const std::vector<double>& x, 
                    const std::vector<double>& y, 
                    size_t order) {
        if (x.size() != y.size()) {
            throw std::runtime_error("x and y must have same size");
        }
        return math::poly::fit(x.size(), x.data(), y.data(), order);
    }, "x"_a, "y"_a, "order"_a,
    "Fit 1D polynomial from arrays");
    
    // 1D fit from VectorDouble
    m.def("fit", [](const VectorDouble& x, const VectorDouble& y, size_t order) {
        return math::poly::fit<VectorDouble>(x, y, order);
    }, "x"_a, "y"_a, "order"_a,
    "Fit 1D polynomial from VectorDouble");
    
    // 2D fit from std::vector
    m.def("fit", [](const std::vector<double>& x,
                    const std::vector<double>& y,
                    const std::vector<double>& z,
                    size_t orderX, size_t orderY) {
        if (x.size() != y.size() || x.size() != z.size()) {
            throw std::runtime_error("x, y, and z must have same size");
        }
        // Assuming data is in row-major order with square layout
        size_t n = x.size();
        size_t numRows = static_cast<size_t>(std::sqrt(n));
        size_t numCols = numRows;
        return math::poly::fit(numRows, numCols, x.data(), y.data(), z.data(), orderX, orderY);
    }, "x"_a, "y"_a, "z"_a, "orderX"_a, "orderY"_a,
    "Fit 2D polynomial from arrays");
    
    // 2D fit from MatrixDouble
    m.def("fit", [](const MatrixDouble& x,
                    const MatrixDouble& y,
                    const MatrixDouble& z,
                    size_t orderX, size_t orderY) {
        return math::poly::fit(x, y, z, orderX, orderY);
    }, "x"_a, "y"_a, "z"_a, "orderX"_a, "orderY"_a,
    "Fit 2D polynomial from MatrixDouble");
}
