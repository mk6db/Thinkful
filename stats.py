import pandas as pd
from scipy import stats

data = '''Region, Alcohol, Tobacco
North, 6.47, 4.03
Yorkshire, 6.13, 3.76
Northeast, 6.19, 3.77
East Midlands, 4.89, 3.34
West Midlands, 5.63, 3.47
East Anglia, 4.52, 2.92
Southeast, 5.89, 3.20
Southwest, 4.79, 2.71
Wales, 5.27, 3.53
Scotland, 6.08, 4.51
Northern Ireland, 4.02, 4.56'''

data = data.splitlines()

data = [i.split(', ') for i in data]

column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns = column_names)

df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

alc_mean = df['Alcohol'].mean()
alc_median = df['Alcohol'].median()
alc_mode = stats.mode(df['Alcohol'])
alc_range = max(df['Alcohol']) - min(df['Alcohol'])
alc_std = df['Alcohol'].std()
alc_var = df['Alcohol'].var()

tbc_mean = df['Tobacco'].mean()
tbc_median = df['Tobacco'].median()
tbc_mode = stats.mode(df['Tobacco'])
tbc_range = max(df['Tobacco']) - min(df['Tobacco'])
tbc_std = df['Tobacco'].std()
tbc_var = df['Tobacco'].var()

print "The mean for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_mean,tbc_mean)
print "The median for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_median,tbc_median)
print "The mode for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_mode[0][0],tbc_mode[0][0])
print "The range for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_range,tbc_range)
print "The standard deviation for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_std,tbc_std)
print "The variance for the Alcohol and Tobacco dataset is {0} for Alochol data and {1} for Tobacco data.".format(alc_var,tbc_var)