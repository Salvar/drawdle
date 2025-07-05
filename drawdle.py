import argparse


def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        words = [line.strip().lower() for line in f if line.strip() and len(line.strip()) == 5 and line.strip().isalpha()]
    return words


def color_row(answer, guess):
    answer = answer.lower()
    guess = guess.lower()
    colors = ["GRAY"] * len(guess)
    answer_chars = list(answer)
    guess_chars = list(guess)
    for i in range(len(guess_chars)):
        if guess_chars[i] == answer_chars[i]:
            colors[i] = "GREEN"
            answer_chars[i] = None
            guess_chars[i] = None
    for i in range(len(guess_chars)):
        if guess_chars[i] is not None and guess_chars[i] in answer_chars:
            colors[i] = "YELLOW"
            idx = answer_chars.index(guess_chars[i])
            answer_chars[idx] = None
    return colors

def pre_filter(words, answer, pattern):
    answer = answer.lower()
    pattern = [c.upper() for c in pattern]

    # Count required letters and identify excluded letters
    required = {}
    excluded = set()
    for i, p in enumerate(pattern):
        letter = answer[i]
        if p in ("G", "Y"):
            required[letter] = required.get(letter, 0) + 1
        else:  # X
            # only exclude if this letter isn't needed elsewhere
            if letter not in required:
                excluded.add(letter)

    filtered = []
    for word in words:
        w = word.lower()
        skip = False
        # position checks
        for i, p in enumerate(pattern):
            if p == "G" and w[i] != answer[i]:
                skip = True
                break
            if p != "G" and w[i] == answer[i]:
                skip = True
                break
        if skip:
            continue
        if any(ch in w for ch in excluded):
            continue
        for ch, cnt in required.items():
            if w.count(ch) < cnt:
                skip = True
                break
        if not skip:
            filtered.append(word)
    return filtered


def find_guess(answer, pattern, words):
    target = [c.upper() for c in pattern]
    candidates = pre_filter(words, answer, target)
    for word in candidates:
        res = color_row(answer, word)
        code = ['G' if c == 'GREEN' else 'Y' if c == 'YELLOW' else 'X' for c in res]
        if code == target:
            return word
    return None


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
