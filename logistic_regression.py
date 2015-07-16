import statsmodels.api as sm
import pandas as pd 
import numpy as np
import math
import matplotlib.pyplot as plt

loansDataClean = pd.read_csv('loansData_clean.csv')

loansDataClean['IR_TF'] = np.where(loansDataClean['Interest.Rate'] <= 0.12, 1, 0)

loansDataClean['intercept'] = 1.0

ind_vars = ['intercept','FICO.Score','Amount.Requested']

print loansDataClean[0:5]

logit = sm.Logit(loansDataClean['IR_TF'], loansDataClean[ind_vars])

result = logit.fit()

coeff = result.params

print coeff
print coeff[0]
print coeff[1]
print coeff[2]

def logistic_function(FicoScore,LoanAmount):
	p = 1/(1 + math.e**(coeff[0] + coeff[1]*(FicoScore) + coeff[2]*(LoanAmount)))
	return p

print logistic_function(720, 10000)

if logistic_function(720, 10000) < 0.70:
	print "We will likely not attain the loan"
else:
	print "We will likely attain the loan"

t = np.arange(250,900,10)

plt.figure()
plt.plot(t,logistic_function(t,10000))
plt.show()

def pred(FicoScore,LoanAmount):
	p = logistic_function(FicoScore,LoanAmount)
	if p < 0.70:
		print "We will likely not attain the loan with a FICO Score of {0}".format(FicoScore)
	else:
		print "We will likely attain the loan with a FICO Score of {0}".format(FicoScore)

pred(720,10000)
