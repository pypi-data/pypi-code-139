'''

    Download wikipedia dump and extract corpus text into .txt format

    You will need to cover these languages in order to replicate the same bigram positive stats
        ar  cs  eo  fr  hy  ja  lo  nqo  ru  sw  ur
        as  de  es  he  id  kn  ml  or   si  ta  vi
        bn  el  fa  hi  is  ko  ne  pt   sr  th  yi
        cr  en  fi  hu  it  ky  nl  ro   sv  tr  zh


    Create two corpus :
        
        - positive_corpus.txt

            These is the corpus or inputs you will be feeding to the model

            This corpus is needed to ensure your target corpus stats are included in the result
            Since wikipedia is a formal sentences, informal text from social network may failed to 
            be recognized as legit text
            Or text with heavy use of emoji text will not work as well if you only use wikipedia text

        - failed_encoding.txt

            A few examples of failure case

'''
import json
import glob
from collections import defaultdict


def get_ngram(text, n=2):
    bigrams = [''.join(bi) for bi in zip(*[text[i:] for i in range(n)])]
    char_stats = set(bigrams)
    return char_stats

def generate_usable_set(ngrams, n=2):
    high_freq_char = []
    print(len(ngrams))
    ngrams_stats = sorted([ (char, cnt) for char, cnt in ngrams.items() ], key=lambda x:x[1], reverse=True)
    # conver 90% of data
    threshold  = max(ngrams_stats[int(len(ngrams_stats)*0.2) ][1], 5)
    for char, cnt in ngrams.items():
        if cnt > threshold:
            high_freq_char.append(char)
    print('original frequency length',len(high_freq_char),'threshold', threshold)
    print(ngrams_stats[:10], ngrams_stats[int(len(ngrams_stats)*0.99) ])
    high_freq_char = set(high_freq_char)

    failed_bigram = {}
    with open('data/failed_encoding.txt', 'r') as f:
        for sentence in f:
            sentence = sentence.strip().lower()
            bigrams = get_ngram(sentence, n=n)
            for bigram in bigrams:
                if bigram not in failed_bigram:
                    failed_bigram[bigram] = 0
                failed_bigram[bigram] += 1

    high_freq_failed = sorted([ (bigram, cnt)  for bigram, cnt in failed_bigram.items() ], key=lambda x:x[1], reverse=True)
    # remove 80% failed encodings
    for (bigram, _) in high_freq_failed[:int(len(high_freq_failed)*0.2)]:
        if bigram in high_freq_char:
            high_freq_char.remove(bigram)
    print(len(high_freq_char))
    # add positive ngrams
    positive_ngram = {}
    with open('data/positive_corpus.txt', 'r') as f:
        for sentence in f:
            sentence = sentence.strip().lower()
            bigrams = get_ngram(sentence, n=n)
            for bigram in bigrams:
                if bigram not in positive_ngram:
                    positive_ngram[bigram] = 0
                positive_ngram[bigram] += 1

    high_freq_pos = sorted([ (bigram, cnt)  for bigram, cnt in positive_ngram.items() ], key=lambda x:x[1], reverse=True)
    # remove 80% failed encodings
    for (bigram, _) in high_freq_pos[:int(len(high_freq_pos)*0.8)]:
        if bigram not in high_freq_char:
            high_freq_char.add(bigram)
    print('new ngram with positive ',len(high_freq_char))
    high_freq_bigram = list(high_freq_char)
    with open('high_freq_{}gram.json'.format(n), 'w') as f:
        json.dump(high_freq_bigram, f)



def calculate_corpus_stats(corpus_file, ngram=2):
    characters = defaultdict(int)
    total = 0
    weight = 1
    if 'data/' in corpus_file:
        weight = 100
    with open(corpus_file, 'r') as f:
        for line in f:
            if len(line) > 80 or weight > 0:
                line = line.strip().replace('\n',' ').lower()
                bigrams = [''.join(bi) for bi in zip(*[line[i:] for i in range(ngram)])]
                char_stats = set(bigrams)
                total += 1
                for char in char_stats:
                    characters[char] += weight
    return (characters, total)


def generate_neg_ngrams(n=3):
    ngrams, sentences = calculate_corpus_stats('data/failed_encoding.txt', ngram=n)
    ngrams_stats = sorted([ (char, cnt) for char, cnt in ngrams.items() ], key=lambda x:x[1], reverse=True)
    ngrams_stats = ngrams_stats[int(len(ngrams_stats)*0.05):]
    print(len(ngrams_stats))
    ngrams_stats = ngrams_stats[:1000000]
    print(len(ngrams_stats))
    negative_ngrams = [ n for (n,_) in ngrams_stats ]
    with open('neg_freq_{}gram.json'.format(n), 'w') as f:
        json.dump(negative_ngrams, f)

if __name__ == "__main__":
    from multiprocessing import Pool
    raw_corpus_files = list(glob.glob("outputs/*.txt"))
    raw_corpus_files.append('data/positive_corpus.txt')
    print(len(raw_corpus_files))
    characters = defaultdict(int)
    total_sent = 0
    with Pool(32) as pool:
        for (char_stats, sentences) in pool.imap(calculate_corpus_stats, raw_corpus_files):
            total_sent += sentences
            for char, cnt in char_stats.items():
                characters[char] += cnt
 
    print(total_sent)
    generate_usable_set(characters, 2)
    generate_neg_ngrams(n=3)

