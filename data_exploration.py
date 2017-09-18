# Exploratory Data Analysis

# Initialise
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

data = pd.read_csv('train1.csv')

def plot_categorical(var1, var2):
    # produces boxplots of var2 against var1
    # var1 is the categorical variable to be plotted on the x-axis
    # var1 must be nominal, does not work on ordinals
    # var2 is the variable to be plotted on the y-axis
    # both take strings as inputs
    temp = data[[c for c in data.columns if c[:len(var1)] == var1]]
    temp = temp.idxmax(axis = 1)
    temp = pd.Series([row[len(var1)+1:] for row in temp], name = var1)
    temp = pd.concat((temp, data[var2]), axis = 1)
    if var1 == "MSSubClass" or var1 == "MoSold":
        xticks = temp[var1].unique().astype(int)
        xticks.sort()
        xticks = [str(i) for i in xticks]
    else:
        xticks = temp[var1].unique()
        xticks.sort()
    fig, ax = plt.subplots(nrows = 2, figsize = (8,6), dpi = 200)
    sns.countplot(x = var1, data = temp, order = xticks, ax = ax[0])
    ax[0].set_xlabel("")
    sns.boxplot(x = var1, y = var2, data = temp, order = xticks, ax = ax[1])
    plt.show()
    
def plot_ordinal(var1, var2):
    temp = data[[var1, var2]]
    fig, ax = plt.subplots(nrows = 2, figsize = (8,6), dpi = 200)
    sns.countplot(x = var1, data = temp, ax = ax[0])
    ax[0].set_xlabel("")
    sns.boxplot(x = var1, y = var2, data = temp, ax = ax[1])
    plt.show()

def plot_correlation_heatmap(var_list):
    # var_list takes a list of variable names as strings
    temp = pd.DataFrame()
    for var in var_list:
        temp = pd.concat((temp, data[[c for c in data.columns if var in c]]),
                         axis = 1)
    corMatrix = temp.corr()
    fig, ax = plt.subplots(figsize = (8,6))
    sns.heatmap(corMatrix, ax = ax, vmin = -1, vmax = 1, 
                mask = np.zeros_like(corMatrix, dtype = np.bool),
                cmap = sns.diverging_palette(220, 20, as_cmap = True), 
                square = True)

plot_categorical("MSSubClass", "SalePrice")
plot_categorical("MSZoning", "SalePrice")
plot_categorical("MoSold", "SalePrice")
plot_categorical("Condition1", "SalePrice")
plot_categorical("Condition2", "SalePrice")
plot_categorical("BldgType", "SalePrice")
plot_categorical("HouseStyle", "SalePrice")
plot_categorical("RoofStyle", "SalePrice")
plot_categorical("RoofMatl", "SalePrice")

plot_ordinal("Utilities", "SalePrice")
plot_ordinal("Functional", "SalePrice")
plot_ordinal("BsmtFinType1", "SalePrice")
plot_ordinal("BsmtFinType2", "SalePrice")

plot_correlation_heatmap(['MSSubClass', 'MSZoning', 'SalePrice'])
plot_correlation_heatmap(['Overall', 'Functional', 'TotRmsAbvGrd', 'Age_House', 'Reconstructed', 'SalePrice'])
plot_correlation_heatmap(['Garage', 'SalePrice'])
plot_correlation_heatmap(['Bsmt', 'SalePrice'])
plot_correlation_heatmap(['Street', 'Alley', 'Lot', 'Land', 'SalePrice'])
plot_correlation_heatmap(['Bldg', 'House', 'SalePrice'])
plot_correlation_heatmap(['Exter', 'SalePrice'])