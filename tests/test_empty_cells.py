"""Compile the native core and test value-less cells across parsing buffers.

Run from a compiler-enabled shell with Python 3 and C++17. The generated XLSX
fixtures contain only synthetic values. Each case runs in its own process.
"""
from pathlib import Path
import argparse
import os
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = (
    '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
    '<dimension ref="A1:C1"/><sheetData><row r="1">'
)
SUFFIX = '</row></sheetData></worksheet>'
FIRST = '<c r="A1"><v>7</v></c>'
LAST = '<c r="C1"><v>11</v></c>'


def write_fixture(path, cells):
    relationships = 'http://schemas.openxmlformats.org/package/2006/relationships'
    office = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    parts = {
        '[Content_Types].xml': (
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" '
            'ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>'
        ),
        '_rels/.rels': (
            f'<Relationships xmlns="{relationships}">'
            f'<Relationship Id="rId1" Type="{office}/officeDocument" '
            'Target="xl/workbook.xml"/></Relationships>'
        ),
        'xl/workbook.xml': (
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            f'xmlns:r="{office}">'
            '<sheets><sheet name="Control" sheetId="1" r:id="rId1"/></sheets></workbook>'
        ),
        'xl/_rels/workbook.xml.rels': (
            f'<Relationships xmlns="{relationships}">'
            f'<Relationship Id="rId1" Type="{office}/worksheet" '
            'Target="worksheets/sheet1.xml"/></Relationships>'
        ),
        'xl/worksheets/sheet1.xml': PREFIX + cells + SUFFIX,
    }
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as package:
        for name, content in parts.items():
            package.writestr(name, content)


def compile_driver(compiler, folder):
    executable = folder / ('empty-cells.exe' if os.name == 'nt' else 'empty-cells')
    sources = [ROOT / 'tests/empty_cells.cpp', ROOT / 'src/XlsxFile.cpp',
               ROOT / 'src/XlsxSheet.cpp', ROOT / 'src/miniz/miniz.cpp']
    if Path(compiler).stem.lower() == 'cl':
        command = [compiler, '/nologo', '/O2', '/DNDEBUG', '/EHsc', '/std:c++17',
                   '/FIcstring', '/FIarray', '/I' + str(ROOT / 'src'),
                   *map(str, sources), '/Fe' + str(executable)]
    else:
        command = [compiler, '-O2', '-DNDEBUG', '-std=c++17', '-pthread',
                   '-include', 'cstring', '-include', 'array', '-I', str(ROOT / 'src'),
                   *map(str, sources), '-o', str(executable)]
    subprocess.run(command, cwd=folder, check=True)
    return executable


def regression_cases():
    empty_cells = {
        'self-closing-cell': '<c r="B1" s="0"/>',
        'closed-cell': '<c r="B1" s="0"></c>',
        'self-closing-value': '<c r="B1"><v/></c>',
        'closed-value': '<c r="B1"><v></v></c>',
        'uncached-formula': '<c r="B1"><f>A1+1</f></c>',
        'empty-inline-string': '<c r="B1" t="inlineStr"><is><t></t></is></c>',
    }
    cases = [('numeric-control', FIRST + '<c r="B1"><v>11</v></c>', 'adjacent')]
    cases.append(('inline-text-control', FIRST + '<c r="B1" t="inlineStr"><is><t>hello</t></is></c>' + LAST, 'text'))
    cases.append(('cached-text-control', FIRST + '<c r="B1" t="str"><v>hello</v></c>' + LAST, 'text'))
    for name, empty in empty_cells.items():
        cases.append((name, FIRST + empty + LAST, 'gap'))
        implicit = empty.replace(' r="B1"', '')
        cases.append((name + '-implicit', FIRST + implicit + '<c><v>11</v></c>', 'gap'))
    for offset in (-2, 0, 2):
        empty = empty_cells['closed-cell']
        padding = (32768 - len(PREFIX + FIRST) + offset) % 32768
        cases.append((f'buffer-boundary-{offset}', FIRST + ' ' * padding + empty + LAST, 'gap'))
    return cases


def check_parser(executable, folder, cases):
    failures = []
    for name, cells, expectation in cases:
        path = folder / (name + '.xlsx')
        write_fixture(path, cells)
        for threads in (1, 2, 10):
            result = subprocess.run([str(executable), str(path), str(threads), expectation],
                                    capture_output=True, text=True, timeout=30)
            if result.returncode:
                failures.append((name, threads, result.returncode, result.stdout, result.stderr))
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'cl' if os.name == 'nt' else 'c++'))
    arguments = parser.parse_args()
    cases = regression_cases()
    with tempfile.TemporaryDirectory(prefix='sheetreader-tests-') as temporary:
        folder = Path(temporary)
        executable = compile_driver(arguments.cxx, folder)
        failures = check_parser(executable, folder, cases)
    for failure in failures:
        print(failure)
    print(f'{len(cases) * 3 - len(failures)}/{len(cases) * 3} parser checks passed')
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
