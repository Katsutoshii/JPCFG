# JPCFG

Japanese Probabilistic Context Free Grammar

Requires: Python 3.6

To install all dependencies, run `pip install -r requirements.txt` from the root.

## Usage instructions

The program should be run as follows from the root directory `JPCFG`:

Run `python src/main.py pcfg` to test the PCFG on the Aozora corpus.

Run `python src/main.py seg` to test the Segmenter on the Aozora corpus.

Run `python src/main.py full` to test both.

See `data/out.txt` for lots of evidence of the program running and creating parse trees.
