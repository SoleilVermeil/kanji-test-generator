# Kanji Test Generator

## Description
The Kanji Test Generator is a command-line tool designed to generate tests for kanji. It provides a convenient way to create customizable tests with specific configurations. Every test generated comes also with the solution.

## Usage
To use the Kanji Test Generator, follow the instructions below:

1. Install the necessary dependencies.
2. Run the script with the desired arguments.

### Installation
To install the Kanji Test Generator, perform the following steps:

1. Clone the repository: `git clone https://github.com/your-username/kanji-test-generator.git`
2. Navigate to the project directory: `cd kanji-test-generator`
3. Install the required dependencies: `pip install -r requirements.txt`

### Command-line Arguments
The Kanji Test Generator accepts the following command-line arguments:

- `-l`, `--language`: Specifies the language of the translations that should appear. Actually the only available values are `en` and `fr`. Note that you can add your own language by adding a column to the file `words.csv`.
- `-t`, `--title`: Specifies the title of the generated document. The default value is "Kanji test".
- `-st`, `--subtitle`: Specifies the subtitle of the generated document. Here, the default value uses $\LaTeX$ formatting and is "`\begin{CJK}{UTF8}{min}漢字検定\end{CJK}`".
- `-i`, `--instructions`: Specifies the instruction given to the student. The default value is "Complete the table below.".
- `-c`, `--columns`: Specifies the number of columns in the test. This argument is **required**.
- `-r`, `--rows`: Specifies the number of rows in the test. This argument is **required**.
- `-d`, `--dir`: Specifies the name of the folder to store the output. The default value is `output`.
- `-s`, `--seed`: Specifies the seed for the random generator. The default value is -1. Change this value to any number to have a deterministic output.

Also note that for technical reasons, the product of the number of rows and columns should be even (ie. they should not be both odd).

### Examples

To generate a kanji test with 4 columns and 5 rows, run the following command:
```
python kanji_test_generator.py -c 4 -r 5
```

To generate the files inside `example/` of this repository, the following command was used:

```
python nihongo.py --title "Example of exam" --subtitle "(c) \\texttt{SoleilVermeil}" --columns 4 --rows 4 --dir example --seed 42 --instructions "Fill the following table. When there is a word, draw the corresponding kanji. When there is a kanji drawn, write the corresponding definition." --language en
```