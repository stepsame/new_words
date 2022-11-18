import re
import sys
from collections import Counter
from functools import lru_cache

import fitz
from word_forms.word_forms import get_word_forms


def get_book_words(file_path):
    if file_path.endswith('.txt'):
        with open(file_path) as f:
            words = f.read().split()
        return words
    elif file_path.endswith('.pdf'):
        words = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text()
                words.extend(text.split())
            return words
    else:
        print('not supported file type!')
        return []


def get_known_words():
    with open('my_known_words.txt') as f:
        words = f.read().splitlines()
        words_set = set(words)
    return words_set


@lru_cache(maxsize=100000)
def is_known_word(word):
    if word.lower() in KNOWN_WORDS:
        return True
    # get word family
    word_forms = get_word_forms(word.lower())
    for word_form_set in word_forms.values():
        if word_form_set.intersection(KNOWN_WORDS):
            return True
    return False


KNOWN_WORDS = get_known_words()


def main():
    if len(sys.argv) != 2:
        return
    file_path = sys.argv[1]
    print("file path", file_path)
    words = get_book_words(file_path)
    word_count = len(words)
    new_words_count = 0
    new_words_list = []
    for word in words:
        if "'" in word or "’" in word:
            continue
        if word.isnumeric():
            continue
        if not any(c.isalpha() for c in word):
            continue
        if len(word) > 30:
            continue
        if word.startswith(("http", "www.")):
            continue
        # valid_word = re.sub(r'\W+', '', word)
        valid_word = word.strip('.#,!?"/()-:“”…’;—‘')
        if valid_word and not is_known_word(valid_word) and not valid_word[0].isupper():
            new_words_count += 1
            new_words_list.append(valid_word)
    new_words_counter = Counter(new_words_list)

    new_word_freq = new_words_count / word_count
    print(f'new words frequency is {new_words_count}/{word_count} = {new_word_freq:.2%}')
    print("new words counter", new_words_counter.most_common(100))


if __name__ == "__main__":
    main()
