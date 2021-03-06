#!/usr/bin/env python3

import argparse
import json
import os

import pandas as pd


"""
%% survey

| type             | name | label                        |
| ---              | ---  | ---                          |
| text             | name | What is your name?           |
| integer          | age  | How old are you?             |
| select_one foods | food | What is your favourite meal? |

%% choices

| list_name | name  | label |
| ---       | ---   | ---   |
| foods     | pasta | Pasta |
| foods     | pizza | Pizza |
| foods     | sushi | Sushi |

%% settings

| form_title |
| ---        |
| Basics     |
"""


def slice_into_sheets(file_content, sep='%%'):
    list_of_sheets = [
        strip_empty(x.split('\n'))
        for x in strip_empty(file_content.split(sep))
    ]
    sheets = {}
    for sheet in list_of_sheets:
        sheets[sheet[0].strip()] = sheet[1:]
    return sheets


def get_dict_of_df_sheets(sheets):
    updated_sheets = {}
    for sheet_name, table in sheets.items():
        columns, _, *content = table
        list_cols = get_list_of_cells(columns)
        list_content = get_list_of_cells(strip_empty(content))

        all_content = [
            {k: v for k, v in zip(list_cols, line)} for line in list_content
        ]
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


def get_sheet_from_json(content, sheet):
    _sheet = []
    for item in content[sheet]:
        new_item = {}
        for k, v in item.items():
            if k.startswith('$') or k == 'select_from_list_name':
                continue
            if k in content['translated']:
                if (
                    len(content['translated']) == len(content['translations'])
                ) and not (
                    len(content['translations']) == 1
                    and content['translations'][0] is None
                ):
                    for val, trans in zip(v, content['translations']):
                        new_item[f'{k}::{trans}'] = val
                else:
                    new_item[k] = v[0]
                continue
            new_item[k] = v

        if 'type' in item and item['type'] in ['select_one', 'select_multiple']:
            new_item['type'] = f"{item['type']} {item['select_from_list_name']}"

        _sheet.append(new_item)

    return _sheet


def order_sheet(sheet_dict, sheet_name):
    df = pd.DataFrame(sheet_dict)
    cols = list(df.columns)
    if sheet_name == 'survey':
        cols.remove('type')
        cols = ['type'] + cols
        return df[cols]
    elif sheet_name == 'choices':
        cols.remove('list_name')
        cols = ['list_name'] + cols
        return df[cols]
    return df


def from_md(in_file, sep='%%'):
    with open(in_file, 'r') as f:
        xlsform = f.read()
    sheets_dict = slice_into_sheets(xlsform, sep=sep)
    return get_dict_of_df_sheets(sheets_dict)


def from_excel(in_file):
    return pd.read_excel(in_file, index_col=None, sheet_name=None)


def from_json(in_file):
    with open(in_file, 'r') as f:
        content = json.loads(f.read())

    sheets = ['survey', 'choices', 'settings']
    project = {}
    for sheet in sheets:
        if not sheet in content or not content[sheet]:
            continue
        if sheet in ['survey', 'choices']:
            project[sheet] = order_sheet(
                get_sheet_from_json(content, sheet), sheet
            )
        else:
            project[sheet] = order_sheet([content[sheet]], sheet)

    return project


def to_excel(project, out_file):
    with pd.ExcelWriter(out_file) as writer:
        for sheet_name, df in project.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def to_md(project, out_file, sep='%%'):
    out = []
    for k, v in project.items():
        out.append(f'{sep} {k}')
        v = v.fillna('')
        out.append(v.to_markdown(index=False, tablefmt='github'))

    with open(out_file, 'w') as f:
        f.write('\n\n'.join(out))


def _get_extension(filename):
    return filename.split('.')[-1]


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to XLSForm')
    parser.add_argument(
        '--input', '-i', type=str, help='Input file, either md, xlsx or json'
    )
    parser.add_argument(
        '--output', '-o', type=str, help='Output XLSForm, either xlsx or md'
    )
    parser.add_argument(
        '--input-separator',
        '-is',
        type=str,
        default='%%',
        help='Markdown sheet separator character',
    )
    parser.add_argument(
        '--output-separator',
        '-os',
        type=str,
        default='%%',
        help='Markdown sheet separator character',
    )
    args = parser.parse_args()

    cwd = os.getcwd()
    in_file = os.path.join(cwd, args.input)
    out_file = os.path.join(cwd, args.output)

    if not _get_extension(out_file) in ['xlsx', 'md']:
        out_file = f'{out_file}.xlsx'

    if in_file.endswith('.md'):
        project = from_md(in_file, sep=args.input_separator)
    if _get_extension(in_file) in ['xls', 'xlsx']:
        project = from_excel(in_file)
    elif in_file.endswith('.json'):
        project = from_json(in_file)

    if out_file.endswith('.xlsx'):
        to_excel(project, out_file)
    elif out_file.endswith('.md'):
        to_md(project, out_file, sep=args.output_separator)


if __name__ == '__main__':
    main()

