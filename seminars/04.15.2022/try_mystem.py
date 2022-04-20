import time
from pathlib import Path

from pymystem3 import Mystem


def main():
    mystem = Mystem()

    # news from https://www.nn.ru/text/education/2022/04/07/71171432/
    plain_text_path = Path(__file__).parent / 'test.txt'

    with plain_text_path.open(encoding='utf-8') as f:
        plain_text = f.read()

    lemmatized_tokens = mystem.lemmatize(plain_text)

    print(type(lemmatized_tokens))  # list

    for token in lemmatized_tokens:
        print(token)

    print(f'Before: {plain_text}')
    print(f'After: {" ".join(lemmatized_tokens)}')

    very_strange_text = '<!@html><body><h1>Hello&@#$ my friend!'
    print(mystem.lemmatize(very_strange_text))

    plain_text_analysis = mystem.analyze(plain_text)
    print(type(plain_text_analysis))

    for i in plain_text_analysis:
        try:
            morphological_analysis = i['analysis'][0]['gr']
            print(i['analysis'][0]['lex'], morphological_analysis)
        except KeyError:
            print(f'Error with retrieving information for <{i}>')

    start = time.time()
    raw_tokens = plain_text.split()
    analysis_result = []
    for token in raw_tokens:
        analysis_result.append(mystem.analyze(token))

    # It takes approximately 60 seconds on lector's machine
    print(f'Time for analyzing each token separately with single instance of Mystem: {time.time() - start : .2f} sec')

    start = time.time()
    analysis_result = mystem.analyze(plain_text)
    # It takes approximately 3 seconds on lector's machine
    print(f'Time for analyzing big text as a whole: {time.time() - start : .2f} sec')

    # Task 1. Cleanup text from any punctuation marks
    # Task 1. Find all unique punctuation marks
    # Task 1. Calculate unique punctuation marks
    # Task 1. Calculate number of nouns
    # Task 1. Are there more nouns than adjectives in a given text?


if __name__ == '__main__':
    main()
