# Feature engineering based on results in data_exploration

# Initialise
import numpy as np
import pandas as pd
data = pd.read_csv('train1.csv')

# Drop Utilities column because only 1 observation in the training set has a
# different value than all others
data = data.drop('Utilities', axis = 1)

# Drop Condition1 and Condition2 because majority of the observations fall
# under Norm
data = data.drop(data[[c for c in data.columns if "Condition" in c]], axis = 1)

# Drop RoofMatl because less than 10 observations in training set have value
# that is not CompShg
data = data.drop(data[[c for c in data.columns if "RoofMatl" in c]], axis = 1)

# Recode Functional into a binary category (Tyical (8) = 1, Others = 0)
data.loc[data['Functional'] < 8, 'Functional'] = 0
data.loc[data['Functional'] == 8, 'Functional'] = 1

# Combine non-residential MSZoning levels into "Others"
temp = data[[c for c in data.columns if "MSZoning" in c]]
data = data.drop(temp.columns, axis = 1)
temp = temp.idxmax(axis = 1)
temp = pd.Series([row[len("MSZoning")+1:] for row in temp], name = "MSZoning")
MSZoning_list = ['RH', 'RL', 'RP', 'RM']
for index, val in enumerate(temp):
    if str(val) not in MSZoning_list:
        temp[index] = "Other"
    else:
        continue
data = pd.concat((data, temp), axis = 1)
del temp, index, val

# Combine roof styles into 3 levels (Gable, Hip, and Other)
temp = data[[c for c in data.columns if "RoofStyle" in c]]
data = data.drop(temp.columns, axis = 1)
temp = temp.idxmax(axis = 1)
temp = pd.Series([row[len("RoofStyle")+1:] for row in temp], name = "RoofStyle")
RoofStyle_list = ['Gable', 'Hip']
for index, val in enumerate(temp):
    if str(val) not in RoofStyle_list:
        temp[index] = "Other"
    else:
        continue
data = pd.concat((data, temp), axis = 1)
del temp, index, val

# Write to csv file
data.to_csv('train1.csv', index = False)