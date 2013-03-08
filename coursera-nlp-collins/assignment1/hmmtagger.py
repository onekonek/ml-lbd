import model
from math import log
import sys
from collections import defaultdict


def lookup_word(hmmmodel, word):
    if word not in hmmmodel.vocabulary:
        # return "_RARE_"
        return model.get_word_class(word)
    else:
        return word


def viterbi(sentence, hmmmodel):
    pi = defaultdict(model.epsilon)
    bp = dict()
    pi[(0, '*', '*')] = 0.0
    tags = ["X" for x in sentence]
    for j, word in enumerate(sentence):
        vword = lookup_word(hmmmodel, word)
        i = j + 1
        utags = hmmmodel.tags
        if i == 1:
            utags = ["*"]
        for u in utags:
            for v in hmmmodel.tags:
                wtags = hmmmodel.tags
                if i < 3:
                    wtags = ["*"]
                (p_max, w_max) = max([(pi[(i - 1, w, u)] +
                                       log(hmmmodel.gram_prob[(w, u, v)]) +
                                       log(hmmmodel.tag_word_prob[(v, vword)]),
                                       w) for w in wtags])
                pi[(i, u, v)] = p_max
                bp[(i, u, v)] = w_max
    (p_max, u, v) = max([(pi[(len(sentence), u, v)] +
                          log(hmmmodel.gram_prob[(u, v, "STOP")]),
                          u,
                          v) for u in hmmmodel.tags for v in hmmmodel.tags])
    tags[-1] = v
    tags[-2] = u
    for i in range(len(sentence) - 2, 0, -1):
        tags[i - 1] = bp[(i + 2, tags[i], tags[i + 1])]
    return tags


if __name__ == '__main__':
    modelfilename = sys.argv[1]
    hmmmodel = model.get_model(modelfilename)
    tagfilename = sys.argv[2]
    sentence = []
    with open(tagfilename, "r") as f:
        for line in f:
            word = line.strip()
            if word == "":
                tags = viterbi(sentence, hmmmodel)
                for (word, tag) in zip(sentence, tags):
                    print word + " " + tag
                print ""
                sentence = []
                continue
            else:
                sentence.append(word)
