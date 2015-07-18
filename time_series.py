import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

#loads data from lending club into dataframe
df = pd.read_csv('C:\Users\Michael\projects\LoansData\LoanStats3b.csv\LoanStats3b.csv')

#converts string to datetime object in pandas
df['issue_d_format'] = pd.to_datetime(df['issue_d'])
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

#plot loan_count_summary
plt.figure()
loan_count_summary.plot()
plt.show(1)
sm.graphics.tsa.plot_acf(loan_count_summary)
plt.show(2)
sm.graphics.tsa.plot_pacf(loan_count_summary)
plt.show(3)

def shift(a):
	shift = pd.Series([])
	for k, val in enumerate(a):
		if k!= 0:
			nn = val - b
			shift[k-1] = nn
		b = val
	return shift

shift_one = shift(loan_count_summary)
shift_two = shift(shift_one)
shift_three = shift(shift_two)

sm.graphics.tsa.plot_acf(shift_one)
plt.show(4)
sm.graphics.tsa.plot_pacf(shift_one)
plt.show(5)
sm.graphics.tsa.plot_acf(shift_two)
plt.show(6)
sm.graphics.tsa.plot_pacf(shift_two)
plt.show(7)
sm.graphics.tsa.plot_acf(shift_three)
plt.show(8)
sm.graphics.tsa.plot_pacf(shift_three)
plt.show(9)