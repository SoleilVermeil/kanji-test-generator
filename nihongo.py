import pandas as pd
from math import floor
import random
import os
import argparse
import sys

# +-----------------------+
# | Setting up the parser |
# +---------------------- +

parser = argparse.ArgumentParser(
    description="This program gnerates a test in order to evaluate the knowledge of kanjis of students. This program generates a LaTeX file made of grids that the students have to fill. These files are then automatically converted into a PDF if pdflatex is available on the current computer. In order to find out if pdflatex is correcly installed, try running 'pdflatex -v'. If it raises an error, you can install pdflatex (on Ubuntu) using 'sudo apt-get install texlive-latex-base'.",
)

parser.add_argument("-l", "--language", type=str, default="en", help="Language of the test", choices=["fr", "en"])
parser.add_argument("-t", "--title", type=str, default="Kanji test", help="Title of the document")
parser.add_argument("-st", "--subtitle", type=str, default=r"\begin{CJK}{UTF8}{min}漢字検定\end{CJK}", help="Subtitle of the document")
parser.add_argument("-i", "--instructions", type=str, default="Complete the table below.", help="Instructions for the students")
parser.add_argument("-c", "--columns", type=int, help="Number of columns", required=True)
parser.add_argument("-r", "--rows", type=int, help="Number of rows", required=True)
parser.add_argument("-o", "--dir", type=str, help="Name of the folder to store the generated files", default="dir")
parser.add_argument("-s", "--seed", type=int, help="Seed for the random generator", default=-1)

# TODO
# Add field "kanji2word ratio and word2kanji ratio (default 0.5 and 0.5)"
# Add field "kanji2word score (default 1)"
# Add field "word2kanji score (default 1)"

args = parser.parse_args()

# +--------------------------------------------+
# | Importing files and sorting the valid rows |
# +--------------------------------------------+

df_ = pd.read_csv("words.csv", sep=";")

# +------------------------------------------------------------+
# | Defining some variables for the generation of the document |
# +------------------------------------------------------------+

DOCUMENT: str = None
with open("model/document.txt", "r") as f:
    DOCUMENT = f.read()

CONTENT: str = None
with open("model/content.txt", "r") as f:
    CONTENT = f.read()

WORD: str = None
with open("model/word.txt", "r") as f:
    WORD = f.read()

# TODO : improve the following code to make it more clear  
assert args.seed >= -1, "The seed must be a positive integer or -1"
if args.seed >= 0:
    seed = args.seed
    random.seed(seed)
elif args.seed == -1:
    seed = random.randrange(sys.maxsize)
    random.seed(seed)

# +------------------------------------------------------------------------+
# | Setting some variables. They will then influence which rows are picked |
# +------------------------------------------------------------------------+

COLS = args.columns
ROWS = args.rows

assert COLS * ROWS % 2 == 0, "The product of the number of rows and columns must be even"

FONTSIZE = int(200 / COLS)
TRUEFALSE = [True] * int(COLS * ROWS / 2) + [False] * int(COLS * ROWS / 2)
random.shuffle(TRUEFALSE)

# +------------------------------------------------------------+
# | Picking rows according to the previously chosen parameters |
# +------------------------------------------------------------+

df = df_.sample(COLS * ROWS)

# +-------------------------+
# | Generating the document |
# +-------------------------+

for version in ["test", "solution"]:

    rows = []

    for i in range(ROWS * COLS):
        jp = df.iloc[i]["jp"]
        fr = df.iloc[i][args.language]
        word = WORD.replace("@JP@", jp).replace("@FR@", fr).replace("@FONTSIZE@", str(FONTSIZE))
        if version == "test":
            if TRUEFALSE[i]:
                word = word.replace("@COLTITLE@", "black").replace("@COLUPPER@", "white")
            else:
                word = word.replace("@COLTITLE@", "white").replace("@COLUPPER@", "black")
        elif version == "solution":
            word = word.replace("@COLTITLE@", "black").replace("@COLUPPER@", "black")
        else:
            raise ValueError("Version must be 'test' or 'solution'")
        rows.append(word)
        
    content = CONTENT.replace("@COLS@", str(COLS)).replace("@WORDS@", "\n".join(rows))

    document = DOCUMENT.replace("@CONTENT@", content)
    
    document = document.replace("@TITLE@", args.title)
    document = document.replace("@SUBTITLE@", args.subtitle)
    document = document.replace("@INSTRUCTIONS@", args.instructions)
    document = document.replace("@POINTS@", str(COLS * ROWS))

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
        
    with open(os.path.join(args.dir, f"{version}.tex"), "w") as f:
        f.write(document)

with open(os.path.join(args.dir, f"params.txt"), "w") as f:
    for arg in vars(args):
        if arg == "seed":
            f.write(f"{arg}: {repr(seed)}\n")
        else:
            f.write(f"{arg}: {repr(getattr(args, arg))}\n")

# +---------------------------------------------------+
# | Converts the .tex file to a .pdf using 'pdflatex' |
# +---------------------------------------------------+

os.system(f"cd {args.dir} && pdflatex test.tex && pdflatex solution.tex && cd ..")
os.system(f"cd {args.dir} && rm *.tex *.aux *.log && cd ..")

print("Done !")