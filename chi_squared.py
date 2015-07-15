import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import collections

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

loansData.dropna(inplace = True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])

chi, p = stats.chisquare(freq.values())
print "Chi equals {0} and p equals {1}".format(chi,p)