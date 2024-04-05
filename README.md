# SheetReader
SheetReader is a blazingly fast and memory-efficient spreadsheet parser for tabular data from Excel OOXML (.xlsx) files, implemented in C++. Other spreadsheet parsers are based on general-purpose XML parsers, that lead to CPU and memory over-utilization, because of the redundant XML information and the inflated in-memory XML tree representation. In contrast, SheetReader leverages the fixed spreadsheet structure, employs parallelism at different levels, and manages memory efficiently. 

## Bindings
We also provide bindings for several environments:
- [R language](https://github.com/fhenz/SheetReader-r/): load spreadsheets into dataframes, also available via [CRAN](https://cran.r-project.org/package=SheetReader)
- [Python language](https://github.com/polydbms/sheetreader-python): load spreadsheets into Pandas dataframes.
- [PostgreSQL FDW](https://github.com/polydbms/pg_sheet_fdw): execute SQL on spreadsheets & combine spreadsheets with DBMS tables

## Paper
SheetReader was published in the [Information Systems Journal](https://www.sciencedirect.com/science/article/abs/pii/S0306437923000194)
```
@article{DBLP:journals/is/GavriilidisHZM23,
  author       = {Haralampos Gavriilidis and
                  Felix Henze and
                  Eleni Tzirita Zacharatou and
                  Volker Markl},
  title        = {SheetReader: Efficient Specialized Spreadsheet Parsing},
  journal      = {Inf. Syst.},
  volume       = {115},
  pages        = {102183},
  year         = {2023},
  url          = {https://doi.org/10.1016/j.is.2023.102183},
  doi          = {10.1016/J.IS.2023.102183},
  timestamp    = {Mon, 26 Jun 2023 20:54:32 +0200},
  biburl       = {https://dblp.org/rec/journals/is/GavriilidisHZM23.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

## Acknowledgements
SheetReader includes and uses the following C/C++ libraries:  
- [miniz](https://github.com/richgel999/miniz) for ZIP archive operations and decompression
- [libdeflate](https://github.com/ebiggers/libdeflate) for optimized full-buffer decompression
- [fast_double_parser](https://github.com/lemire/fast_double_parser) for optimized number parsing