#!/usr/bin/env python
# Example uses of permtst

from perm_stat import *


# One-Sample Tests: the following example, and output from various commercial
# packages, is provided by Gibbons and Chakraborti (2003, pg. 218-220).

before = [51.2,46.5,24.1,10.2,65.3,92.1,30.3,49.2]
after  = [45.8,41.3,15.8,11.1,58.5,70.3,31.6,35.4]
after = [92.0, 75.8, 66.7, 52.2, 85.3,  75.0, 100.0, 50.0, 77.8, 100.0, 18.9,
        45.5, 14.3, 91.7, 66.7]
before = [33.3, 66.8, 100.0, 42.6, 79.2, 75.0, 100.0, 34.6, 53.8, 100.0, 17.1,
        30.0, 12.0, 82.4, 53.6]
after =  [93.5, 78.0, 90.1, 00.0, 97.0, 50.0, 66.7, 95.7, 100.0,50.0, 94.7, 95.2, 100.0,93.3, 91.7, 82.4, 100.0, 88.0]
before = [73.4, 61.4, 85.8, 14.3, 91.2, 50.0, 73.7, 90.9, 100.0,50.0, 69.2, 80.0, 100.0,60.9, 61.5, 46.7, 94.7, 76.9]
diff   = d = [a - b for b, a in zip(before, after)] # = after - before

print "- - - - - - - One Sample Tests - - - - - - -"
print " "

print "fisher permutation test:"
print ["avg < 0","avg > 0","avg != 0"]
print fisher_perm_test(diff)
print " "

print "wilcoxon permutation test:"
print ["avg < 0","avg > 0","avg != 0"]
print wilcoxon_perm_test(diff)
print " "


# Two-Sample Tests: the following example, and output from various commercial
# packages, is provided by Gibbons and Chakraborti (2003, pg. 303-305).

treatment_x = [12.6,11.4,13.2,11.2,09.4,12.0]
treatment_y = [16.4,14.1,13.4,15.4,14.0,11.3]

print "- - - - - - - Two Sample Tests - - - - - - -"
print " "

print "pitman permutation test:"
print ["avg(x) < avg(y)","avg(x) > avg(y)","avg(x) != avg(y)"]
print pitman_perm_test(treatment_x,treatment_y)
print " "

print "wilcoxon-mann-whitney permutation test:"
print ["avg(x) < avg(y)","avg(x) > avg(y)","avg(x) != avg(y)"]
print wmw_perm_test(treatment_x,treatment_y)


# References
#
# @book{
# address = {New York},
# author = {Gibbons, Jean Dickinson and Chakraborti, Subhabrata},
# edition = {4},
# publisher = {Marcel Dekker, Inc.},
# title = {{Nonparametric Statistical Inference}},
# year = {2003}
# } 
