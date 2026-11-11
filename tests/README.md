# Empty-cell regression tests

Run `python tests/test_empty_cells.py` in a C++17 compiler shell. On Windows,
use the Visual Studio x64 developer shell. On other platforms the default
compiler is `c++`. Set `CXX` or pass `--cxx` to select another compiler.

The runner builds the native core in a temporary directory and creates synthetic
XLSX fixtures. Each fixture runs in a fresh process with one, two and ten parser
threads. The driver checks values and coordinates through the public row iterator.

The cases cover self-closing and explicit empty cells, absent formula caches,
empty value elements, inline strings, implicit cell coordinates and parsing-buffer
boundaries. Invalid numeric input must report a failed parse. Text and numeric
controls check that the next value remains intact after the parser state resets.
