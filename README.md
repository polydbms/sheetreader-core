# SheetReader
<p align="center">
  <img src="logo-sheetreader.png" width="200">
</p>

SheetReader is a fast, memory-efficient spreadsheet parser for tabular data from Excel OOXML (.xlsx) files, implemented in C++. Unlike many existing spreadsheet loaders, which rely on general-purpose XML parsers, SheetReader is designed specifically for spreadsheet data. By exploiting the fixed structure of .xlsx files, using parallelism at multiple levels, and managing memory carefully, it avoids unnecessary XML overhead and enables efficient ingestion of spreadsheet data.

## Bindings

We provide bindings for several environments:

- [R](https://github.com/fhenz/SheetReader-r/): load spreadsheets into data frames. Also available on [CRAN](https://cran.r-project.org/package=SheetReader).
- [Python](https://github.com/polydbms/sheetreader-python): load spreadsheets into pandas DataFrames. Also available on [PyPI](https://pypi.org/project/pysheetreader/).
- [PostgreSQL FDW](https://github.com/polydbms/pg_sheet_fdw): access spreadsheets from PostgreSQL through a foreign data wrapper and combine them with other PostgreSQL tables. Also available on [PGXN](https://pgxn.org/dist/pg_sheet_fdw/).
- [DuckDB extension](https://github.com/polydbms/sheetreader-duckdb): access spreadsheets from DuckDB and combine them with other DuckDB tables. Also available as a [community extension](https://duckdb.org/community_extensions/extensions/sheetreader.html).

## Scientific Background
SheetReader was introduced in the **PolyDB research project** ([polydbms.org](https://polydbms.org)). The initial design and evaluation was published in the **Information Systems Journal**. If you use SheetReader in your research, consider citing the following paper:
```bibtex
@article{GavriilidisHZM23,
  author       = {Haralampos Gavriilidis and Felix Henze and Eleni Tzirita Zacharatou and Volker Markl},
  title        = {SheetReader: Efficient Specialized Spreadsheet Parsing},
  journal      = {Inf. Syst.},
  volume       = {115},
  pages        = {102183},
  year         = {2023},
  url          = {https://doi.org/10.1016/j.is.2023.102183}
}
```

## Acknowledgements
SheetReader includes and uses the following C/C++ libraries:  
- [miniz](https://github.com/richgel999/miniz) for ZIP archive operations and decompression
- [libdeflate](https://github.com/ebiggers/libdeflate) for optimized full-buffer decompression
- [fast_double_parser](https://github.com/lemire/fast_double_parser) for optimized number parsing

Logo design by Stefanie Lenk.