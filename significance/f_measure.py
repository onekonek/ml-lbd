#!/usr/bin/env python
# Example uses of permtst

from perm_stat import *


# One-Sample Tests: the following example, and output from various commercial
# packages, is provided by Gibbons and Chakraborti (2003, pg. 218-220).

after  = [90.2, 86.0, 66.7, 61.5, 81.7,  85.7, 40.0, 64.3, 73.7, 33.3, 31.8,
    52.6, 18.2, 81.5, 66.7]
before = [13.3, 79.9, 50.0, 58.2, 82.6,  85.7, 40.0, 50.0, 60.9, 33.3, 29.2,
    42.9, 18.2, 80.0, 65.2]
diff   = d = [a - b for a, b in zip(before, after)] # = before - after

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

#treatment_x = [12.6,11.4,13.2,11.2,09.4,12.0]
#treatment_y = [16.4,14.1,13.4,15.4,14.0,11.3]

#print "- - - - - - - Two Sample Tests - - - - - - -"
#print " "

#print "pitman permutation test:"
#print ["avg(x) < avg(y)","avg(x) > avg(y)","avg(x) != avg(y)"]
#print pitman_perm_test(treatment_x,treatment_y)
#print " "

#print "wilcoxon-mann-whitney permutation test:"
#print ["avg(x) < avg(y)","avg(x) > avg(y)","avg(x) != avg(y)"]
#print wmw_perm_test(treatment_x,treatment_y)


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
