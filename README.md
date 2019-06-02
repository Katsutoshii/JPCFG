# JPCFG

Japanese Probabilistic Context Free Grammar

Requires: Python 3

## Usage instructions

Run all files from the root of this directory.

Make sure that the `src` directory is added to the Python Path. (In PyCharm, right-click and select "Mark as sources root").
Alternatively, run `set PYTHONPATH=./src` or `export PYTHONPATH=./src` in the terminal when at the root of this project.

Run `python src/main.py pcfg` to test the PCFG on the Aozora corpus.

Run `python src/main.py seg` to test the Segmenter on the Aozora corpus.

Run `python src/main.py full` to test both.
