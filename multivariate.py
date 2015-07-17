import statsmodels.api as sm
import pandas as pd 
import numpy as np
import math
import matplotlib.pyplot as plt

#load data from LendingClub
loansData = pd.read_csv('C:\Users\Michael\projects\MultivariateAnalysis\LoanStats3d.csv\LoanStats3d.csv')

#create dataframe with required columns
subLoans = pd.DataFrame(columns = ['InterestRate','AnnualIncome','HomeOwnership'])
subLoans['InterestRate'] = loansData['int_rate']
subLoans['AnnualIncome'] = loansData['annual_inc']
subLoans['HomeOwnership'] = loansData['home_ownership']

#clean data of NAs
subLoans.dropna(inplace=True)

#adjust format of columns and adding boolean for HomeOwnership and adding intercept
subLoans['InterestRate'] = subLoans['InterestRate'].map(lambda x: round(float(x.rstrip('%'))/100,4))
subLoans['HomeOwnBool'] = np.where(subLoans['HomeOwnership'] == "MORTGAGE", 1, 0)
subLoans['Intercept'] = float(1.0)

#using income to model interest rates
model = sm.OLS(subLoans['InterestRate'] ,subLoans[['Intercept','AnnualIncome']])
f = model.fit()

print f.summary()

#adding home ownership to the model
model2 = sm.OLS(subLoans['InterestRate'],subLoans[['Intercept','AnnualIncome','HomeOwnBool']])
f2 = model2.fit()

print f2.summary()

#interaction term
subLoans['Interaction'] = subLoans['AnnualIncome'] * subLoans['HomeOwnBool']
model3 = sm.OLS(subLoans['InterestRate'],subLoans[['Intercept','AnnualIncome','HomeOwnBool','Interaction']])
f3 = model3.fit()

print f3.summary()