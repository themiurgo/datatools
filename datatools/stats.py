import numpy
from scipy.stats import pearsonr
import sys

data = numpy.genfromtxt("prova.txt", delimiter=',')
[name1,name2,pearson_coeff,pearson_2t_p_value,spearman]
for col1, col2 in itertools.combinations(range(data.shape[1]), 2):
    print col1, col2, pearsonr(data[:,col1], data[:,col2])