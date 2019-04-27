import random
import sys
from collections import deque


def load_lines(f):
	txt = ' '.join(l.strip() for l in f)
	return txt.replace(',', '').replace(';', '.').replace('!','.').replace('?','.').replace('--', ' ').replace('\'', '').replace('_', '').split('.')


def make_markov_model(lines, ngram):
	model = {}
	for line in lines:
		line = line.split()
		for i in range(len(line)-ngram):
			for j in range(1, ngram+1):
				key = tuple(line[i:i+j])
				next_word = line[i+j]
				try:
					model[key].append(next_word)
				except KeyError:
					model[key] = [next_word]
	return model


def main():
	fname = sys.argv[1]
	length = int(sys.argv[2])
	ngram = int(sys.argv[3])
	with open(fname) as f:
		model = make_markov_model(load_lines(f), ngram)
		keys = list(model)
		last_words = deque(random.choice(keys), ngram)
		for _ in range(length):
			key = tuple(last_words)
			for i in range(ngram):
				if key[i:] in model:

					word = random.choice(model[key[i:]])
					break
			else:

				word = random.choice(random.choice(keys))

			last_words.append(word)
			sys.stdout.write('{} '.format(word))
	print()


if __name__ == '__main__':
	main()
