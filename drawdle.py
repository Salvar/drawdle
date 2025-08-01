import argparse
import random

def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip() and len(line.strip()) == 5 and line.strip().isalpha()]
    return words

def color_row(answer, guess):
    # Returns pattern like ['G', 'Y', 'X', 'X', 'G']
    answer = answer.lower()
    guess = guess.lower()
    colors = ['X'] * 5
    answer_chars = list(answer)
    guess_chars = list(guess)

    # First pass: Green
    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            colors[i] = 'G'
            answer_chars[i] = None
            guess_chars[i] = None

    # Second pass: Yellow
    for i in range(5):
        if guess_chars[i] is not None and guess_chars[i] in answer_chars:
            colors[i] = 'Y'
            answer_chars[answer_chars.index(guess_chars[i])] = None

    return colors

def find_guess(answer, pattern, words):
    target = [c.upper() for c in pattern]
    candidates = [word for word in words if color_row(answer, word) == target]
    return random.choice(candidates) if candidates else None

def parse_pattern(text):
    mapping = {
        'G': 'G', 'GREEN': 'G',
        'Y': 'Y', 'O': 'Y', 'ORANGE': 'Y', 'YELLOW': 'Y',
        'X': 'X', 'B': 'X', 'GRAY': 'X', 'GREY': 'X', 'BLACK': 'X'
    }
    text = text.strip().upper()
    parts = [mapping.get(ch, None) for ch in text.split() if ch]
    if len(parts) == 5 and all(p in 'GYX' for p in parts):
        return parts
    if len(text) == 5 and all(ch in mapping for ch in text):
        return [mapping[ch] for ch in text]
    raise ValueError("Pattern must be 5 characters or 5 space-separated codes")

def main():
    parser = argparse.ArgumentParser(description="Find Wordle guesses that match given color patterns.")
    parser.add_argument('answer', help='Secret answer word')
    parser.add_argument('--words', default='words.txt', help='Path to word list file')
    args = parser.parse_args()
    words = load_words(args.words)

    print("Enter up to 6 pattern rows (5 chars each). Use G for green, Y for yellow/orange, X for gray. Blank line to stop.")
    patterns = []
    while len(patterns) < 6:
        row = input(f"Row {len(patterns)+1}: ").strip()
        if not row:
            break
        try:
            patt = parse_pattern(row)
            patterns.append(patt)
        except ValueError as e:
            print(e)
            continue

    for i, patt in enumerate(patterns):
        guess = find_guess(args.answer, patt, words)
        if guess:
            print(f"Guess for row {i+1}: {guess}")
        else:
            print(f"No guess found for row {i+1}")


if __name__ == '__main__':
    main()
