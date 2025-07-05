# drawdle

This repository contains a small utility for generating Wordle guesses that match a desired color pattern for a given answer.

## reverse_wordle.py

The `reverse_wordle.py` script reads a secret answer and a set of color patterns and finds dictionary words that would yield those patterns when guessed in Wordle.

### Usage

```
python reverse_wordle.py ANSWER
```

When run, the script prompts for up to six pattern rows. Each row is a five-character string using:

- `G` for green (correct letter, correct position)
- `Y` for yellow/orange (correct letter, wrong position)
- `X` for gray/dark (letter not present)

Press Enter on an empty line to stop entering patterns. For every row provided, a possible guess is printed.

A word list is required to generate guesses. By default `words.txt` is used (included in this repo). You can specify a different list with `--words PATH`.

### Example

```
$ python reverse_wordle.py crane
Enter up to 6 pattern rows (5 chars each). Use G for green, Y for yellow/orange, X for gray. Blank line to stop.
Row 1: XGYXX
Row 2:
Guess for row 1: breds
```

The script found `breds` as a valid guess that produces the pattern `XGYXX` when the answer is `crane`.
