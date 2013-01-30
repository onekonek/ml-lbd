from ex6 import transform_samples, read_samples, phi
from lregression import Regression


def eval(samples, classifier):
  n_correct = 0
  n_false = 0
  n_total = 0
  for x in samples.keys():
      res = classifier.classify([1] + list(x))
      if ((res < 0 and samples[x] < 0)
              or (res > 0 and samples[x] > 0)):
          n_correct += 1
          n_total += 1
      else:
          n_false += 1
          n_total += 1
  return n_correct, n_false, n_total



if __name__ == '__main__':

    in_samples_validate = transform_samples(
        read_samples("in.dta", end=25), phi)
    in_samples_train = transform_samples(
        read_samples("in.dta", start=25), phi)
    out_samples = transform_samples(
        read_samples("out.dta"), phi)
    k = range(2, 8)
    for i in k:
      in_k_train = {s[:i]:in_samples_train[s] for s in in_samples_train}
      in_k_validate = {s[:i]:in_samples_validate[s] for s in
          in_samples_validate}
      out_k_samples = {s[:i]:out_samples[s] for s in out_samples}
      lreg = Regression()
      lreg.train(in_k_train)
      n_correct_val, n_false_val, n_total_val = eval(in_k_validate, lreg)
      n_correct_out, n_false_out, n_total_out = eval(out_k_samples, lreg)
      print "{0} E_val {1}".format(i, float(n_false_val) / n_total_val)
      print "{0} E_out {1}".format(i, float(n_false_out) / n_total_out)
