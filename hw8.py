from libsvm.svm import *
import itertools
import numpy
from libsvm.svmutil import *


def load_zip_data(filename):
  data = open(filename, "r")
  y = []
  x = []
  for line in data:
    cols = line.split()
    y.append(float(cols[:1][0]))
    x.append([float(f) for f in cols[1:]])
  return y, x


def one_vs_all_zip(y, x, one):
  y_res = []
  x_res = []
  for label, features in zip(y, x):
    if (int(label) == int(one)):
      y_res.append(+1)
      x_res.append(features)
    else:
      y_res.append(-1)
      x_res.append(features)
  y_res, x_res = zip(*sorted(zip(y_res, x_res)))
  return y_res, x_res

def one_vs_one_zip(y, x, one, other):
  y_res = []
  x_res = []
  for label, features in zip(y, x):
    if (int(label) == int(one)):
      y_res.append(+1)
      x_res.append(features)
    elif (int(label) == int(other)):
      y_res.append(-1)
      x_res.append(features)
  y_res, x_res = zip(*sorted(zip(y_res, x_res)))
  return y_res, x_res


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    chunks = []
    for i in xrange(0, len(l), n):
        chunks.append(l[i:i+n])
    return chunks

def cross_validate_sets(y, x, k):
  s = zip(y, x)
  numpy.random.shuffle(s)
  s_chunks = chunks(s, len(s) / k)
  validate_sets = []
  train_sets = []
  for i in range(k):
    validate_sets.append(s_chunks[i])
    s = []
    for j in range(k):
      if i != j:
       s += s_chunks[j]
    train_sets.append(s)
  return train_sets, validate_sets

def ex8(y_1_vs_5_train, x_1_vs_5_train, y_1_vs_5_test, x_1_vs_5_test):
  models = []
  train_sets, val_sets = cross_validate_sets(y_1_vs_5_train, x_1_vs_5_train, 10)
  C = [0.01, 1.0, 100.0, 10.0**4, 10.0**6]
  for i, c in enumerate(C):
    all_prob = svm_problem(y_1_vs_5_train, x_1_vs_5_test)
    all_param = svm_parameter('-h 0 -q -t 2 -g 1 -c ' + str(c))
    all_m = svm_train(all_prob, all_param)
    models.append(all_m)
    e_out.append(0.0)
    e_in.append(0.0)
    e_cv.append(0.0)
    e_out[i] = eval(all_m, y_1_vs_5_test, x_1_vs_5_test)
    e_in[i] = eval(all_m, y_1_vs_5_train, x_1_vs_5_train)
    for train, val in zip(train_sets, val_sets):
      y, x = zip(*train)
      y_val, x_val = zip(*val)
      prob = svm_problem(y, x)
      param = svm_parameter('-h 0 -q -t 2 -g 1 -c ' + str(c))
      m = svm_train(prob, param)
      e_cv[i] += eval(m, y_val, x_val)
    e_cv[i] = e_cv[i] / 10.0
  for i, c in enumerate(C):
    print "C:{0} e_cv:{1} e_out:{2} e_in:{3} n_svs:{4}\n".format(c, e_cv[i],
        e_out[i], e_in[i], len(models[i].get_SV()))


def ex5(y_1_vs_5_train, x_1_vs_5_train, y_1_vs_5_test, x_1_vs_5_test):
  models = []
  train_sets, val_sets = cross_validate_sets(y_1_vs_5_train, x_1_vs_5_train, 10)
  C = [0.01, 1.0, 100.0, 10.0**4, 10.0**6]
  Q = [2, 5]
  # C = [0.1]
  e_cv = []
  e_out = []
  e_in = []
  s = ""
  for q in Q:
    for i, c in enumerate(C):
      all_prob = svm_problem(y_1_vs_5_train, x_1_vs_5_test)
      all_param = svm_parameter('-h 0 -q -t 1 -d ' + str(q) + ' -r 1 -g 1 -c ' + str(c))
      all_m = svm_train(all_prob, all_param)
      models.append(all_m)
      e_out.append(0.0)
      e_in.append(0.0)
      e_cv.append(0.0)
      e_out[i] = eval(all_m, y_1_vs_5_test, x_1_vs_5_test)
      e_in[i] = eval(all_m, y_1_vs_5_train, x_1_vs_5_train)
      for train, val in zip(train_sets, val_sets):
        y, x = zip(*train)
        y_val, x_val = zip(*val)
        prob = svm_problem(y, x)
        param = svm_parameter('-h 0 -q -t 1 -d 2 -r 1 -g 1 -c ' + str(c))
        m = svm_train(prob, param)
        e_cv[i] += eval(m, y_val, x_val)
      e_cv[i] = e_cv[i] / 10.0
    for i, c in enumerate(C):
      s += "Q:{0} C:{1} e_cv:{2} e_out:{3} e_in:{4} n_svs:{5}\n".format(q, c, e_cv[i],
          e_out[i], e_in[i], len(models[i].get_SV()))
    print s




def ex2(y_l_vs_all_train, x_l_vs_all_train, y_l_vs_all_test, x_l_vs_all_test):
  models = []
  e_in = []
  for y, x in zip(y_l_vs_all_train, x_l_vs_all_train):
    prob = svm_problem(y, x)
    param = svm_parameter('-h 0 -q -t 1 -d 2 -r 1 -g 1 -c 0.01')
    m = svm_train(prob, param)
    models.append(m)
    e_in.append(eval(m, y, x))
  for i, (e, m) in enumerate(zip(e_in, models)):
    svs = m.get_SV()
    print "{0} vs all: E_in {1}, n_sv {2}".format(i, e, len(svs))

def eval(model, y, x):
  p_label, p_acc, p_val = svm_predict(y, x, model)
  correct = 0
  for p_l, a_l in zip(p_label, y):
    if (p_l == a_l):
      correct += 1
  return (len(y) - correct) / float(len(y))

if __name__ == '__main__':
  y_train, x_train = load_zip_data('features.train')
  y_test, x_test = load_zip_data('features.train')
  y_l_vs_all_train = []
  x_l_vs_all_train = []
  y_l_vs_all_test = []
  x_l_vs_all_test = []
  for l in range(10):
    y_l_train, x_l_train = one_vs_all_zip(y_train, x_train, l)
    y_l_test, x_l_test = one_vs_all_zip(y_test, x_test, l)
    y_l_vs_all_train.append(y_l_train)
    x_l_vs_all_train.append(x_l_train)
    y_l_vs_all_test.append(y_l_test)
    x_l_vs_all_test.append(x_l_test)
  y_1_vs_5_train, x_1_vs_5_train = one_vs_one_zip(y_train, x_train, 1, 5)
  y_1_vs_5_test, x_1_vs_5_test = one_vs_one_zip(y_test, x_test, 1, 5)
  #ex2(y_l_vs_all_train, x_l_vs_all_train, y_l_vs_all_test, x_l_vs_all_test)
  #ex8(y_1_vs_5_train, x_1_vs_5_train, y_1_vs_5_test, x_1_vs_5_test)
  ex5(y_1_vs_5_train, x_1_vs_5_train, y_1_vs_5_test, x_1_vs_5_test)


