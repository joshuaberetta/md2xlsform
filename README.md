# md2xlsform

Convert Markdown to XLSForm for importing into KoBo.

## Setup
```bash
git clone https://github.com/joshuaberetta/md2xlsform
cd md2xlsform
pip3 install -r requirements.txt

# optional
chmod +x md2xlsform.py
sudo ln -s $(pwd)/md2xlsform.py /usr/local/bin/md2xlsform
```

## Usage
```bash
# if added to path
md2xlsform -i input_file.md -o output_file.xlsx

# otherwise
./md2xlsform.py -i input_file.md -o output_file.xlsx
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

%% settings

| form_title |
| ---        |
| Basics     |
```
