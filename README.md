# md2xlsform

Convert Markdown to XLSForm for importing into KoBo

## Setup
```
chmod +x md2xlsform.py
sudo ln -s $(pwd)/md2xlsform.py /usr/local/bin/md2xlsform
```

## Usage
```
md2xlsform -i input_file.md -o output_file.xlsx
```

## Markdown file structure

```markdown
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
```
