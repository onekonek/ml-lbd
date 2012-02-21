
import math
import collections


_NINF = float('-1e300')

_START_VALUE = "<start>"
_END_VALUE = "<end>"

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
                if index + i == 0:
                    features['ww[%i]_%s'% (i, _START_VALUE)] = 1
                elif index + i == len(sentence):
                    features['ww[%i]_%s'% (i, _END_VALUE)] = 1
                elif 0 < index + i < len(sentence):
                    features['ww[%i]_%s'% (i, sentence[index + i].string)] = 1
        if ('pw' in self.feature_config.keys()):
            for i in range(self.pw_start, self.pw_end + 1):
                if index + i == 0:
                    features['pw[%i]_%s'% (i, _START_VALUE)] = 1
                elif index + i == len(sentence):
                    features['pw[%i]_%s'% (i, _END_VALUE)] = 1
                elif 0 < index + i < len(sentence):
                    features['pw[%i]_%s'% (i, sentence[index + i].tags["POS"])] = 1
        if ('suf' in self.feature_config.keys()):
            for i in range(1, self.suf_len + 1):
                if i < len(sentence[index].string) + 1:
                    features['suf[-%i]_%s'% (i, sentence[index].string[-i:])] = 1
        return features


class FrequencyMap(object):

    def __init__(self):
        self._total = 0
        self._freq_map = collections.defaultdict(int)

    def inc(self, element, count = 1):
        self._freq_map[element] += count 
        self._total += count

    def dec(self, element):
        if self._freq_map[element] > 0:
            self._freq_map[element] -= 1
            self._total -=1

    def total(self):
        return self._total

    def freq(self, element):
        return self._freq_map[element]

    def keys(self):
        return self._freq_map.keys()

    def print_stats(self):
      print "Total: {0}\n".format(self._total)
      for el, freq in sorted(self._freq_map.iteritems(), key=lambda x: x[1],
                             reverse = True):
          print "{0:<10}: {1:>10} {2:>7.2f}%".format(el, self._freq_map[el],
                                         float(self._freq_map[el]*100)/self._total)

class FeatureMap(object):

    def __init__(self):
        self._next_index = 0
        self._fmap = {}
        self._rev_fmap = []

    def get(self, id):
        if id in self._fmap:
            return self._fmap[id]
        else:
            self._fmap[id] = self._next_index
            self._rev_fmap.append(id)
            self._next_index += 1
            return self._fmap[id]

    def get_rev(self, id):
        if id < len(self._rev_fmap):
            return self._rev_fmap[id]
        else:
            return None

    def keys(self):
        return self._fmap.keys()

class ProbDist(object):

    def __init__(self):
        self._prob = {}


    def set(self, element, probability):
        self._prob[element] = probability

    def inc(self, element, probability):
        if element in self._prob:
            self._prob[element] += probability
        else:
            self._prob[element] = probability

    def max(self):
        return max(self._prob.iteritems(), key = lambda x: x[1])

    def logprob(self, element):
        p = self.prob(element)
        if p == 0:
            return _NINF
        else:
            return math.log(p, 2)

    def keys(self):
        return self._prob.keys()

    def prob(self, element):
        if element not in self._prob:
            return 0
        else:
            return self._prob[element]
            
    def print_prob(self):
        print self._prob

