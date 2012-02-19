


class FeatureExtractor():

    def __init__(self, feature_config = {}):
        self.feature_config = feature_config
        self._parse_feature_config()

    def _parse_feature_config(self):
        for key, value in self.feature_config.iteritems():
            if key == 'ww':
                self.ww_start = int(value.split(':')[0])
                self.ww_end = int(value.split(':')[1])
            elif key == 'pw':
                self.pw_start = int(value.split(':')[0])
                self.pw_end = int(value.split(':')[1])
            elif key == 'suf':
                self.suf_len = int(value)

    def extract_features(self, sentence, index):
        """Extract the features at index in the sequence given by sentence."""
        features = {}
        assert(index < len(sentence))
        if ('ww' in self.feature_config.keys()):
            for i in range(self.ww_start, self.ww_end + 1):
                features['ww[%i]_%s'% (i, sentence[index + i].string)] = 1
        if ('pw' in self.feature_config.keys()):
            for i in range(self.pw_start, self.pw_end + 1):
                features['pw[%i]_%s'% (i, sentence[index + i].tags["POS"])] = 1
        if ('suf' in self.feature_config.keys()):
            for i in range(-1, -(self.suf_len + 1), -1):
                features['suf[%i]_%s'% (i, sentence[index].string[i:])] = 1
        return features
