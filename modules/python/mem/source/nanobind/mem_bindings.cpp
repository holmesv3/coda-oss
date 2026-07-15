/*
 * =========================================================================
 * This file is part of mem-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * mem-python is free software; you can redistribute it and/or modify
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

#include "import/mem.h"

namespace nb = nanobind;

NB_MODULE(coda_mem, m) {
    m.doc() = "CODA-OSS memory management utilities";
    
    // Note: This module is primarily for C++ API compatibility.
    // The SWIG version provided macros (SHARED, SCOPED_COPYABLE, SCOPED_CLONEABLE)
    // for template instantiation in other modules.
    // 
    // In nanobind, each consuming module handles its own smart pointer bindings
    // directly, so this module serves mainly as a placeholder for compatibility
    // and to ensure the mem C++ library is available to dependent modules.
    //
    // Smart pointer template classes (ScopedCopyablePtr, ScopedCloneablePtr, SharedPtr)
    // should be bound directly in the modules that use them with specific types.
}
