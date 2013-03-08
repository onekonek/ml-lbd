import sys
import re
import math
from collections import defaultdict


def epsilon():
    return math.exp(-550)

class HMMModel():

    def __init__(self):
        self.tags = set()
        self.vocabulary = set()
        self.tag_prob = defaultdict(epsilon)
        self.tag_word_prob = defaultdict(epsilon)
        self.gram_prob = defaultdict(epsilon)


def read_counts_file(filename):
    tags = set()
    vocabulary = set()
    tag_word_counts = defaultdict(int)
    tag_counts = defaultdict(int)
    word_counts = defaultdict(int)
    gram_counts = defaultdict(int)
    with open(filename, "r") as f:
        for line in f:
            cols = line.strip().split()
            typ = cols[1]
            count = int(cols[0])
            if (typ == "WORDTAG"):
                tag_word_counts[(cols[2], cols[3])] = count
                tag_counts[cols[2]] += count
                tags.add(cols[2])
                vocabulary.add(cols[3])
                word_counts[cols[3]] += count
            else:
                gram_counts[tuple(cols[2:])] = count
    return tag_word_counts, tag_counts, word_counts, gram_counts, vocabulary, tags


def calculate_probabilities(tag_word_counts, tag_counts, word_counts,
                            gram_counts, gram_len=3):
    tag_word_prob = defaultdict(epsilon)
    gram_prob = defaultdict(epsilon)
    for (tag, word), count in tag_word_counts.items():
        tag_word_prob[tag, word] = float(count) / tag_counts[tag]
    for (tags), count in gram_counts.items():
        if len(tags) == gram_len:
            gram_prob[tags] = float(count) / gram_counts[tags[:-1]]
    return tag_word_prob, gram_prob


def write_data_replace_rare(outfilename, tag_word_counts, word_counts,
                            gram_counts, mincount=5):
    for (tag, word), count in tag_word_counts.items():
        if word_counts[word] < mincount:
            del tag_word_counts[(tag, word)]
            word = "_RARE_"
            tag_word_counts[(tag, word)] += count
    with open(outfilename, "w") as f:
        for (tag, word), count in tag_word_counts.items():
            f.write("{0} WORDTAG {1} {2}\n".format(count, tag, word))
        for (tags), count in gram_counts.items():
            f.write("{0} {1}-GRAM {2}\n".format(count, len(tags),
                                                " ".join(tags)))


def get_word_class(word):
    if re.search(r'\d', word):
        return "_NUMERIC_"
    elif re.match(r'^[A-Z]+$', word):
        return "_ALLCAPITAL_"
    elif re.match(r'.*[A-Z]$', word):
        return "_ENDCAPITAL_"
    else:
        return "_RARE_"


def write_data_replace_classes(outfilename, tag_word_counts, word_counts,
                               gram_counts, mincount=5):
    for (tag, word), count in tag_word_counts.items():
        if word_counts[word] < mincount:
            del tag_word_counts[(tag, word)]
            word = get_word_class(word)
            tag_word_counts[(tag, word)] += count
    with open(outfilename, "w") as f:
        for (tag, word), count in tag_word_counts.items():
            f.write("{0} WORDTAG {1} {2}\n".format(count, tag, word))
        for (tags), count in gram_counts.items():
            f.write("{0} {1}-GRAM {2}\n".format(count, len(tags),
                                                " ".join(tags)))


def get_model(filename):
    model = HMMModel()
    fname = sys.argv[1]
    (tag_word_counts, tag_counts, word_counts,
     gram_counts, vocabulary, tags) = read_counts_file(fname)
    tag_word_prob, gram_prob = calculate_probabilities(tag_word_counts,
                                                       tag_counts,
                                                       word_counts,
                                                       gram_counts)
    model.tag_word_prob = tag_word_prob
    model.vocabulary = vocabulary
    model.tags = tags
    model.gram_prob = gram_prob
    return model


if __name__ == '__main__':
    fname = sys.argv[1]
    (tag_word_counts, tag_counts, word_counts,
     gram_counts, vocabulary, tags) = read_counts_file(fname)
    if len(sys.argv) > 2:
        outname = sys.argv[2]
        write_data_replace_rare(outname, tag_word_counts, word_counts,
                                gram_counts)
        print "Wrote " + outname
        exit(0)
