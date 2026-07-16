#!/usr/bin/env python3
"""
Validate Python stub files (.pyi) for CODA-OSS nanobind modules.

This script validates that:
1. All .pyi files are syntactically valid Python
2. Stub files can be parsed without errors
3. Basic module imports work (if modules are installed)

Usage:
    python validate_stubs.py [--check-imports]

Options:
    --check-imports    Also try to import and test actual modules (requires installation)
"""

import sys
import ast
import argparse
from pathlib import Path
from typing import List, Tuple

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def validate_stub_syntax(pyi_file: Path) -> Tuple[bool, str]:
    """
    Validate that a .pyi file has valid Python syntax.
    
    Args:
        pyi_file: Path to .pyi file
        
    Returns:
        Tuple of (success, error_message)
    """
    try:
        with open(pyi_file, 'r') as f:
            code = f.read()
        
        # Try to parse the file as Python AST
        ast.parse(code, filename=str(pyi_file))
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error parsing file: {e}"


def find_all_stub_files(base_dir: Path) -> List[Path]:
    """
    Find all .pyi stub files in the modules/python directory.
    
    Args:
        base_dir: Base directory to search (modules/python)
        
    Returns:
        List of Path objects for all .pyi files
    """
    return sorted(base_dir.glob("*/source/**/*.pyi"))


def validate_all_stubs(base_dir: Path) -> bool:
    """
    Validate all stub files.
    
    Args:
        base_dir: Base directory containing Python modules
        
    Returns:
        True if all validations pass, False otherwise
    """
    stub_files = find_all_stub_files(base_dir)
    
    if not stub_files:
        print(f"{YELLOW}⚠ Warning: No .pyi files found in {base_dir}{RESET}")
        return False
    
    print(f"Found {len(stub_files)} stub files to validate\n")
    
    all_passed = True
    passed_count = 0
    failed_count = 0
    
    for pyi_file in stub_files:
        relative_path = pyi_file.relative_to(base_dir)
        success, error_msg = validate_stub_syntax(pyi_file)
        
        if success:
            print(f"{GREEN}✓{RESET} {relative_path}")
            passed_count += 1
        else:
            print(f"{RED}✗{RESET} {relative_path}")
            print(f"  {error_msg}")
            failed_count += 1
            all_passed = False
    
    print(f"\n{'='*60}")
    print(f"Results: {passed_count} passed, {failed_count} failed")
    print(f"{'='*60}")
    
    return all_passed


def test_module_imports() -> bool:
    """
    Test importing actual modules (if installed).
    
    Returns:
        True if tests pass, False otherwise
    """
    print(f"\n{'='*60}")
    print("Testing module imports (requires installation)")
    print(f"{'='*60}\n")
    
    test_modules = [
        ('coda.coda_types', 'RowColDouble'),
        ('coda.coda_except', 'Exception'),
        ('coda.coda_io', 'StringStream'),
        ('coda.coda_mt', 'ThreadGroup'),
        ('coda.coda_sys', 'UTCDateTime'),
        ('coda.coda_xml_lite', 'Element'),
        ('coda.sio_lite', 'FileHeader'),
        ('coda.math_linear', 'Vector3'),
        ('coda.math_poly', 'Poly1D'),
    ]
    
    all_passed = True
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    
    for module_name, test_class in test_modules:
        try:
            module = __import__(module_name, fromlist=[test_class])
            
            # Check that the test class exists
            if hasattr(module, test_class):
                print(f"{GREEN}✓{RESET} {module_name}.{test_class}")
                passed_count += 1
            else:
                print(f"{RED}✗{RESET} {module_name}.{test_class} - class not found")
                failed_count += 1
                all_passed = False
                
        except ImportError as e:
            print(f"{YELLOW}⊘{RESET} {module_name} - not installed (skipping)")
            skipped_count += 1
        except Exception as e:
            print(f"{RED}✗{RESET} {module_name} - error: {e}")
            failed_count += 1
            all_passed = False
    
    print(f"\n{'='*60}")
    print(f"Results: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")
    print(f"{'='*60}")
    
    return all_passed


def test_basic_functionality():
    """
    Test basic functionality of modules if available.
    """
    print(f"\n{'='*60}")
    print("Testing basic module functionality")
    print(f"{'='*60}\n")
    
    tests_run = 0
    tests_passed = 0
    
    # Test coda_types
    try:
        from coda import coda_types
        rc = coda_types.RowColDouble(1.0, 2.0)
        assert rc.row == 1.0 and rc.col == 2.0
        rc2 = rc + coda_types.RowColDouble(3.0, 4.0)
        print(f"{GREEN}✓{RESET} coda_types: RowColDouble arithmetic")
        tests_passed += 1
        tests_run += 1
    except ImportError:
        print(f"{YELLOW}⊘{RESET} coda_types: not installed")
    except Exception as e:
        print(f"{RED}✗{RESET} coda_types: {e}")
        tests_run += 1
    
    # Test coda_xml_lite
    try:
        from coda import coda_xml_lite
        parser = coda_xml_lite.MinidomParser()
        parser.parse("<root><child>text</child></root>")
        doc = parser.getDocument()
        root = doc.getRootElement()
        assert root.getLocalName() == "root"
        print(f"{GREEN}✓{RESET} coda_xml_lite: XML parsing")
        tests_passed += 1
        tests_run += 1
    except ImportError:
        print(f"{YELLOW}⊘{RESET} coda_xml_lite: not installed")
    except Exception as e:
        print(f"{RED}✗{RESET} coda_xml_lite: {e}")
        tests_run += 1
    
    # Test coda_math_linear
    try:
        from coda.math_linear import Vector3, cross
        v1 = Vector3([1.0, 0.0, 0.0])
        v2 = Vector3([0.0, 1.0, 0.0])
        v3 = cross(v1, v2)
        assert v3[2] == 1.0  # Should be [0, 0, 1]
        print(f"{GREEN}✓{RESET} coda_math_linear: Vector3 cross product")
        tests_passed += 1
        tests_run += 1
    except ImportError:
        print(f"{YELLOW}⊘{RESET} coda_math_linear: not installed")
    except Exception as e:
        print(f"{RED}✗{RESET} coda_math_linear: {e}")
        tests_run += 1
    
    # Test coda_math_poly
    try:
        from coda.math_poly import Poly1D
        poly = Poly1D([1.0, 2.0, 3.0])  # 1 + 2x + 3x^2
        result = poly(2.0)
        expected = 1.0 + 2.0*2.0 + 3.0*2.0*2.0  # = 1 + 4 + 12 = 17
        assert abs(result - expected) < 1e-10
        print(f"{GREEN}✓{RESET} coda_math_poly: Poly1D evaluation")
        tests_passed += 1
        tests_run += 1
    except ImportError:
        print(f"{YELLOW}⊘{RESET} coda_math_poly: not installed")
    except Exception as e:
        print(f"{RED}✗{RESET} coda_math_poly: {e}")
        tests_run += 1
    
    if tests_run == 0:
        print(f"{YELLOW}No modules installed for testing{RESET}")
        return True
    
    print(f"\n{'='*60}")
    print(f"Results: {tests_passed}/{tests_run} tests passed")
    print(f"{'='*60}")
    
    return tests_passed == tests_run


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate CODA-OSS Python stub files"
    )
    parser.add_argument(
        '--check-imports',
        action='store_true',
        help='Also test module imports (requires modules to be installed)'
    )
    parser.add_argument(
        '--test-functionality',
        action='store_true',
        help='Run basic functionality tests (requires modules to be installed)'
    )
    
    args = parser.parse_args()
    
    # Find modules/python directory
    script_dir = Path(__file__).parent
    
    print(f"\n{'='*60}")
    print("CODA-OSS Python Stub Validation")
    print(f"{'='*60}\n")
    print(f"Scanning directory: {script_dir}")
    
    # Validate stub file syntax
    syntax_ok = validate_all_stubs(script_dir)
    
    if not syntax_ok:
        print(f"\n{RED}✗ Stub validation failed{RESET}")
        return 1
    
    # Optional: test imports
    if args.check_imports:
        imports_ok = test_module_imports()
        if not imports_ok:
            print(f"\n{YELLOW}⚠ Some import tests failed{RESET}")
    
    # Optional: test functionality
    if args.test_functionality:
        functionality_ok = test_basic_functionality()
        if not functionality_ok:
            print(f"\n{YELLOW}⚠ Some functionality tests failed{RESET}")
    
    print(f"\n{GREEN}✓ All stub files are syntactically valid!{RESET}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
