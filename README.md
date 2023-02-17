# Overview

This repository is used to serve https://typing.derivativeworks.co a simple website to dynamically generate typing speed tests uses a Markov Model for word frequency. The model is trained on a subset of Wikipedia and the generate tests have a nice but non-sensical flow. The output of the model prefers longer words and the 2000 most common English words as defined in `common_words.py`.

# Markov Model

The code for training a new model given a corpus, along with using a model can be found in marcov.py
First insall the module and it's dependencies:
```bash
$ pip install -e .
```
To train a model, run:
```bash
$ python src/markov_typing_test/markov.py make_model /path/to/articles ./output_model.pkl
```

The model will load all `.txt` file in the articles directory and use them to fit next work probabilities for 3,2,and 1 word combinations.

To use the provided Charles Dickens novel run:
```bash
$ python src/markov_typing_test/markov.py make_model ./text/ ./dickens.pkl
```

To generate text run something like:
```bash
$ python src/markov_typing_test/markov.py get_text  ./dickens.pkl 100
she turned her head back towards mr bounderby again how did she come there when it was their hour for going by the instance last given of the popular fictions of coketown which some pains had been required for example little service and much law probably would have done no less if the wood with their pure hands a garden in charge to make mistakes i cant help it i do feel independent now i have supposed him to be at stone lodge aforesaid direction of a certain annual stipend mrs bounderby no you know i have how else was
```

## Limitations
Does not handle capitilization, nor enforce that words are proper english.
The solution to avoice loops where a key maps only too itself, e.g.
`("we're", "stuck", "here") -> ["we're"]`
Was to not allow any keys to map to just one word. There might be other loops but they haven't been observed.

# Server
The dockerfile in `containers/Dockerfile` is configured to run the server on port 5656

```bash
# build
$ docker build -f containers/Dockerfile  -t typing:latest .
# run
$ docker run typing:latest  -p 5656:5656
```
Then you can access the sever at http://0.0.0.0:5656
