
import math
from token import Token, TokenReader
from feature import FeatureExtractor, FrequencyMap, FeatureMap, ProbDist
import itertools
from collections import defaultdict
import evaluate.scores


class NaiveBayesClassifier(object):

    def __init__(self):
        self.label_prob = ProbDist()
        self.label_feat_prob = defaultdict(ProbDist)
        self._fmap = FeatureMap()

    def print_features(self, label):
        for fid in self._fmap.keys():
            if (label, fid) in self.label_feat_prob:
                pdist = self.label_feat_prob[label, fid]
                for val in pdist.keys():
                    print "{0} {1} {2} {3}".format(label, fid, val,
                                                   pdist.prob(val))

    def train(self, label_features_set):
        label_freq_map = FrequencyMap()
        label_fid_freq_map = defaultdict(FrequencyMap)
        for label, features in label_features_set:
            # Count how often the label occurs.
            label_freq_map.inc(label)
            # Count how often a value for a given feature and label occurs.
            for f, val in features.iteritems():
                label_fid_freq_map[label, f].inc(val)
                # Record that we have seen that feature (for some label).
                self._fmap.get(f)

        for label in label_freq_map.keys():
            num_count = label_freq_map.freq(label)
            for f in self._fmap.keys():
                count = label_fid_freq_map[label, f].total()
                label_fid_freq_map[label, f].inc(None, num_count - count)

        # Compute the probabilities.
        for label in label_freq_map.keys():
            # P(label)
            probability = float(label_freq_map.freq(label))/label_freq_map.total()
            self.label_prob.set(label, probability)

        for ((label, f), freqmap) in label_fid_freq_map.items():
             for val in freqmap.keys():
                 p = float(freqmap.freq(val)) / float(freqmap.total())
                 self.label_feat_prob[label, f].set(val, p)

    def classify(self, features):
        features_copy = features.copy()
        for f in features_copy.keys():
            if f not in self._fmap.keys():
                del features_copy[f]
        prob_dist = ProbDist()

        for label in self.label_prob.keys():
            prob_dist.set(label, self.label_prob.logprob(label))
            for feat, val in features_copy.iteritems():
                if (label, feat) not in self.label_feat_prob:
                    print "ERROR"
                p_dist = self.label_feat_prob[label, feat]
                prob_dist.inc(label, p_dist.logprob(val))
        return prob_dist


if __name__ == '__main__':

    reader = TokenReader()
    feature_extractor = FeatureExtractor({'suf':'3'})
    sentences = []
    sentences = reader.read_whitespaced_tokens("data/train_chunk.txt")
    sentences.extend(reader.read_whitespaced_tokens("data/test_chunk.txt"))
    naive_bayes = NaiveBayesClassifier()
    featureset = []
    correct_answers = []
    print "Extracting features."
    for sentence in sentences:
        for i, token in enumerate(sentence):
            features = feature_extractor.extract_features(sentence, i) 
            label = token.tags["POS"]
            featureset.append((label, features))
    print "Extracted for {0} tokens".format(len(featureset))
    size = int(len(featureset) * 0.1)
    train_set, test_set = featureset[size:], featureset[:size]
    print "Training."
    naive_bayes.train(train_set)
    print "Done training."
    result = []
    correct_answers = []
    print "Classifying {0}.".format(len(test_set))
    for label, f in test_set:
        res = naive_bayes.classify(f)
        result.append(res.max()[0])
        correct_answers.append(label)
    print "Done classifying."
    acc = evaluate.scores.accuracy(correct_answers, result)
    print "Accuracy: {0:.4f}".format(acc)


