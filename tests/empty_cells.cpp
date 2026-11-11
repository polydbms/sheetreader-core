#include <array>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include "XlsxFile.h"

// Exercise the public parser and row iterator, including implicit cell positions.
// The closed empty-cell case reproduces the value-length underflow encountered
// in an Enron workbook without including corpus data in the test fixtures.
int main(int argc, char** argv) {
    if (argc != 4) return 2;
    try {
        XlsxFile file(argv[1]);
        file.parseSharedStrings();
        auto sheet = file.getSheet(1);
        sheet.mHeaders = false;
        const bool success = sheet.interleaved(0, 0, std::stoi(argv[2]));
        file.finalize();
        const std::string expectation = argv[3];
        if (expectation == "failure") {
            if (success) throw std::runtime_error("Parser accepted an incomplete result");
            return 0;
        }
        if (!success) throw std::runtime_error("Parser rejected a valid fixture");
        const auto row = sheet.nextRow();
        const size_t lastColumn = expectation == "adjacent" ? 1 : 2;
        if (row.first != 0 || row.second.size() <= lastColumn) {
            throw std::runtime_error("Missing row or column");
        }
        if (row.second[0].type != CellType::T_NUMERIC || row.second[0].data.real != 7
            || row.second[lastColumn].type != CellType::T_NUMERIC
            || row.second[lastColumn].data.real != 11) {
            throw std::runtime_error("Cell values or positions changed");
        }
        if (expectation == "text") {
            const auto& middle = row.second[1];
            if (middle.type != CellType::T_STRING
                || file.getDynamicString(0, middle.data.integer) != "hello") {
                throw std::runtime_error("Text payload changed between numeric cells");
            }
        } else if (lastColumn == 2 && row.second[1].type != CellType::T_NONE) {
            throw std::runtime_error("Empty cell acquired a value");
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
