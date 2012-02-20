from token import Token, TokenReader
from feature import FeatureExtractor, FrequencyMap, FeatureMap

from collections import defaultdict


if __name__ == '__main__':

    reader = TokenReader()
    feature_extractor = FeatureExtractor({'suf':'2'})
    sentences = reader.read_whitespaced_tokens("data/train_pos.txt")
    train_featureset = []
    f_map = FeatureMap()
    label_freq_map = FrequencyMap()
    label_fid_freq_map = defaultdict(FrequencyMap)
    for sentence in sentences:
        for i, token in enumerate(sentence):
            features = feature_extractor.extract_features(sentence, i) 
            label = token.tags["POS"]
            train_featureset.append((label, features))
            label_freq_map.inc(label)
            for f,val in features.iteritems():
                label_fid_freq_map[label].inc(f_map.get(f))
    label_freq_map.print_stats()
    label_fid_freq_map["NN"].print_stats()
