import itertools
import os
import pickle
import random
import sys
from collections import Counter

import fire
from markov_typing_test.common_words import COMMON_WORDS

N_GRAM_MAX = 3


def _process_word(word: str) -> str:
    w = "".join(
        ch for ch in word if ord("A") <= ord(ch) <= ord("z") or ch == "-" or ch == "'"
    ).lower()
    return w


def _make_markov_model(lines, ngram, model=None):
    if model is None:
        model = {}
    for line in lines:
        line = list(map(_process_word, line.strip().split()))
        for i in range(len(line) - ngram):
            for j in range(1, ngram + 1):
                key = tuple(line[i : i + j])
                next_word = line[i + j]
                if key not in model:
                    model[key] = {}
                if next_word not in model[key]:
                    model[key][next_word] = 1
                else:
                    model[key][next_word] += 1
    return model


def make_model(article_dir: str, outfile: str, max_files: int = 2000):
    articles = os.listdir(article_dir)
    random.shuffle(articles)
    model = {}
    for i, article in enumerate(articles):
        print(f"Processing {article}")
        with open(os.path.join(article_dir, article)) as fo:
            lines = [l.rstrip() for l in fo.readlines()]
            lines = [l for l in lines if len(l) > 1]
            model = _make_markov_model(lines, N_GRAM_MAX, model)
            if i % 100 == 0:
                with open(outfile, "wb") as out:
                    print(f"Checkpointing model")
                    pickle.dump(model, out)
            if i > max_files:
                break

    with open(outfile, "wb") as out:
        pickle.dump(model, out)


def _gen_text(model: dict) -> str:
    key = random.choice(list(model.keys()))
    done_words = set()
    while True:
        # TODO weight against choosing the same words again in a less all-or-nothing way
        # TODO try other words at the full key size rather than shortening immediately
        word = _get_word(model, key)
        if word in done_words:
            done_words.pop(word)
        else:
            yield word
            if len(key) == N_GRAM_MAX:
                key = key[1:]
            key = (*key, word)
            if not _valid_key(key, model):
                for i in range(1, N_GRAM_MAX):
                    if _valid_key(tuple(key[i:]), model):
                        key = key[i:]
                        break
                else:
                    print("random")
                    key = random.choice(list(model.keys()))
            # print(key, model[key])


def _valid_key(key: tuple[str], model: dict) -> bool:
    if len(key) == 0:
        return False
    words = model.get(key, None)
    if words is None:
        return False
    elif len(words) == 0:
        return False
    elif len(words) == 1:
        return False
    return True


def _get_word(model, key):
    words, weights = zip(
        *[
            (
                word,
                weight
                * (4 if word in COMMON_WORDS else 1)
                * (4 if len(word) > 3 else 1),
            )
            for word, weight in model[key].items()
        ]
    )
    (word,) = random.choices(words, weights=weights)
    return word


def get_text(model: str, nwords: int = 1000):
    with open(model, "rb") as fo:
        model = pickle.load(fo)

    text = list(itertools.islice(_gen_text(model), nwords))
    print(" ".join(text))


if __name__ == "__main__":
    fire.Fire()
