from token import Token, TokenReader
from feature import FeatureExtractor


if __name__ == '__main__':

    reader = TokenReader()
    feature_extractor = FeatureExtractor({'ww':'-1:1', 'pw':'-1:1', 'suf':'2'})
    tokens = reader.read_whitespaced_tokens("data/train_pos.txt")
    tokens[10].print_tagged()
    print feature_extractor.extract_features(tokens, 10)
