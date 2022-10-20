import itertools
import os
import pickle
import random
import sys
from collections import deque

import fire
import numpy as np

from markov_typing_test.common_words import COMMON_WORDS


def _load_lines(f):
    txt = " ".join(l.strip() for l in f)
    return (
        txt.replace(",", "")
        .replace(";", ".")
        .replace("!", ".")
        .replace("?", ".")
        .replace("--", " ")
        .replace("_", "")
        .split(".")
    )


# common_words = open('')
def _make_markov_model(lines, ngram, model=None):
    if model is None:
        model = {}
    for line in lines:
        line = line.split()
        for i in range(len(line) - ngram):
            for j in range(1, ngram + 1):
                key = tuple(line[i : i + j])
                # if not (set(key) & COMMON_WORDS):
                #   continue
                next_word = line[i + j]
                if next_word not in COMMON_WORDS:
                    continue
                if key not in model:
                    model[key] = {}
                if next_word not in model[key]:
                    model[key][next_word] = 1
                else:
                    model[key][next_word] += 1
    return model


def make_model(article_dir: str, outfile: str):
    # = sys.argv[1]
    # outfile = sys.argv[2]
    articles = os.listdir(article_dir)
    random.shuffle(articles)
    model = {}
    for i, article in enumerate(articles):
        print(f"Processing {article}")
        with open(os.path.join(article_dir, article)) as fo:
            lines = [l.rstrip() for l in fo.readlines()]
            lines = [l for l in lines if len(l) > 1]
            model = _make_markov_model(lines, 3, model)
            if i % 100 == 0:
                with open(outfile, "wb") as out:
                    print(f"Checkpointing model")
                    pickle.dump(model, out)
            if i > 2000:
                return


def _gen_text(model: dict) -> str:
    key = random.choice(list(model.keys()))
    # for _ in range(nwords):
    done_words = set()
    while True:
        # TODO weight against choosing the same words again in a less all-or-nothing way
        word = _get_word(model, key)
        if word in done_words:
            done_words.pop(word)
        else:
            yield word
            key = (*key[1:], word)
            if key not in model:
                print("Random")
                # TODO store lesser ngrams so we can roll back
                key = random.choice(list(model.keys()))


def _get_word(model, key):
    words = list(model[key].keys())
    weights = list(model[key].values())
    # TODO need to use a better structure
    # TODO can do normalization
    weights = weights / np.sum(weights)
    ixs = np.arange(weights.size, dtype=int)
    ix = np.random.choice(ixs, p=weights)
    return words[ix]
    # model[start]
    # ngram = len()[0])


def get_text(model: str, nwords: int = 1000):
    with open(model, "rb") as fo:
        model = pickle.load(fo)
    print(" ".join(itertools.islice(_gen_text(model), nwords)))
    # fname = sys.argv[1]
    # length = int(sys.argv[2])
    # ngram = int(sys.argv[3])
    # with open(fname) as f:
    #     model = make_markov_model(load_lines(f), ngram)
    #     keys = list(model)
    #     last_words = deque(random.choice(keys), ngram)
    #     for _ in range(length):
    #         key = tuple(last_words)
    #         for i in range(ngram):
    #             if key[i:] in model:

    #                 word = random.choice(model[key[i:]])
    #                 break
    #         else:

    #             word = random.choice(random.choice(keys))

    #         last_words.append(word)
    #         sys.stdout.write("{} ".format(word))
    # print()


if __name__ == "__main__":
    fire.Fire()
