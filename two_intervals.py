
from scipy import misc
from sets import Set


for n in range(1, 20):
  test = Set()
  for a in range(0, n + 2):
    for b in range(0, n + 2):
      for x in range(0, n + 2):
        for y in range(0, n + 2):
          seq = ()
          for element in range(1, n + 1):
            if ((a <= element <= b) or (x <= element <= y)):
                seq = seq + (element, )
          test.add(seq)
  print "n: %i len: %i perm: %i" %(n, len(test), misc.comb(n + 1 , 4, exact=1) +
      misc.comb(n + 1, 2, exact=1) + 1)
