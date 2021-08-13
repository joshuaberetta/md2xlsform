#!/usr/bin/env python3

import argparse
import os

import pandas as pd


"""
%% survey

| type                   | name  | label          |
| ---                    | ---   | ---            |
| text                   | hello | hello world    |
| select_one fields      | field | Select a field |
| select_multiple fields | field | Select fields  |

%% choices

| list_name | name | label |
| ---       | ---  | ---   |
| fields    | a    | A     |
| fields    | b    | B     |

%% settings

| form_title        |
| ---               |
| A brave new world |
"""


def slice_into_sheets(file_content):
    list_of_sheets = [
        strip_empty(x.split('\n'))
        for x in strip_empty(file_content.split('%%'))
    ]
    sheets = {}
    for sheet in list_of_sheets:
        sheets[sheet[0].strip()] = sheet[1:]
    return sheets


def get_dict_of_df_sheets(sheets):
    updated_sheets = {}
    for sheet_name, table in sheets.items():
        columns, _, content = table[0], table[1], table[2:]
        content = strip_empty(content)

        list_cols = get_list_of_cells(columns)
        list_content = get_list_of_cells(content)

        all_content = []
        for line in list_content:
            all_content.append({k: v for k, v in zip(list_cols, line)})

        updated_sheets[sheet_name] = pd.DataFrame(all_content)
    return updated_sheets


def strip_empty(content):
    return [line for line in content if line]


def get_cells(line):
    return [cell.strip() for cell in line.split('|') if cell]


def get_list_of_cells(content):
    if isinstance(content, str):
        return get_cells(content)
    return [get_cells(line) for line in content]


def to_excel(in_file, out_file):
    with open(in_file, 'r') as f:
        xlsform = f.read()

    sheets_dict = slice_into_sheets(xlsform)
    sheets_df = get_dict_of_df_sheets(sheets_dict)

    with pd.ExcelWriter(out_file) as writer:
        for sheet_name, df in sheets_df.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to XLSForm')
    parser.add_argument('--input', '-i', type=str, help='Input markdown file')
    parser.add_argument('--output', '-o', type=str, help='Output XLSForm file')
    args = parser.parse_args()

    cwd = os.getcwd()
    in_file = f'{cwd}/{args.input}'
    out_file = f'{cwd}/{args.output}'
    if not out_file.endswith('.xlsx'):
        out_file = f'{out_file}.xlsx'

    to_excel(in_file, out_file)


if __name__ == '__main__':
    main()

