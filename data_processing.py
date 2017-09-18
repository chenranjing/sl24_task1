# Data processing and feature engineering

# Initialise
import pandas as pd

# Read data
file = 'train.csv'
data = pd.read_csv(file)

# Drop variables with considerable number of missing values
data = data.drop(['PoolQC', 'MiscFeature', 'Alley', 'Fence', 'FireplaceQu'], 
                 axis = 1)

# Drop variables with majority zeros
data = data.drop(['PoolArea', '3SsnPorch', 'ScreenPorch', 'EnclosedPorch', 'BsmtFullBath', 'BsmtHalfBath'], axis = 1)

# Delete MiscVal due to large number of zeros and its relation to MiscFeature
data = data.drop('MiscVal', axis = 1)

# Convert MsSubClass from float to object
data['MSSubClass'] = data['MSSubClass'].astype(object)

# Convert MoSold from integer to object
data['MoSold'] = data['MoSold'].astype(object)

# Houses with no lot frontage, value is set to 0
data.loc[data['LotFrontage'].isnull(), 'LotFrontage'] = 0

# Houses with missing values for MasVnrType assumed equal to None; area equal 0
data.loc[data['MasVnrType'].isnull(), 'MasVnrArea'] = 0
data.loc[data['MasVnrType'].isnull(), 'MasVnrType'] = 'None'

# Convert all nominal variables to dummy variables (either 0 or 1)
data['CentralAir'] = (data['CentralAir'] == 'Y').astype(int)
nominal = ['MSSubClass', 'MSZoning', 'Street', 'LandContour', 'LotConfig', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'Heating', 'GarageType', 'SaleType', 'MoSold']
dummies = pd.get_dummies(data[nominal])

# Join dummy variables to dataing set and remove original columns
data = data.join(dummies).drop(nominal, axis = 1)

# Define function to recode ordinal variables into integers
def recode_ordinal(data, colName, levels):
    # data is the name of the variable containing the data frame.
    # colName takes a string input for the name of the ordinal variable.
    # levels takes a list of strings for the different levels in the ordinal
    #   variable, listed from lowest to highest.
    i = 1
    for lvl in levels:
        data.loc[data[colName] == lvl, colName] = i
        i += 1
    data[colName] = data[colName].astype(int) # convert column to integer

# Recode ordinals
recode_ordinal(data, 'LotShape', ['IR3', 'IR2', 'IR1', 'Reg'])
recode_ordinal(data, 'Utilities', ['ELO', 'NoSewa', 'NoSewr', 'AllPub'])
recode_ordinal(data, 'LandSlope', ['Sev', 'Mod', 'Gtl'])
recode_ordinal(data, 'ExterQual', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
recode_ordinal(data, 'ExterCond', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
data.loc[data['BsmtQual'].isnull(), 'BsmtQual'] = 0
recode_ordinal(data, 'BsmtQual', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
data.loc[data['BsmtCond'].isnull(), 'BsmtCond'] = 0
recode_ordinal(data, 'BsmtCond', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
data.loc[data['BsmtExposure'].isnull(), 'BsmtExposure'] = 0
recode_ordinal(data, 'BsmtExposure', ['No', 'Mn', 'Av', 'Gd'])
data.loc[data['BsmtFinType1'].isnull(), 'BsmtFinType1'] = 0
recode_ordinal(data, 'BsmtFinType1', ['Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'])
data.loc[data['BsmtFinType2'].isnull(), 'BsmtFinType2'] = 0
recode_ordinal(data, 'BsmtFinType2', ['Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'])

# credit to Zhehao Zhang for all lines below
#get the age of House
data['Age_House'] = data ['YrSold'] - data ['YearBuilt']
#whether a house had been reconstructed
data ['Reconstructed'] = data ['YearRemod/Add'] - data ['YearBuilt']
# 1- the house had been reconstructed, otherwise 0
data.loc[data ['Reconstructed'] > 0, 'Reconstructed'] = 1

#get the age of Garage
data ['Age_Garage'] = data ['YrSold'] - data ['GarageYrBlt']

# HeatingQC
recode_ordinal (data, 'HeatingQC', ['Po','Fa','TA','Gd','Ex'])
#Electrical
data.loc[data ['Electrical'].isnull(), 'Electrical'] = 0
recode_ordinal (data, 'Electrical', ['Mix','FuseP','FuseF','FuseA','SBrkr'])
#KitchenQual
recode_ordinal (data,'KitchenQual', ['Po','Fa','TA','Gd','Ex'])
#Functional
recode_ordinal (data, 'Functional' ,
                ['Sal','Sev','Maj2','Maj1','Mod','Min2','Min1','Typ'])
#Garage Finish
data.loc[data ['GarageFinish'].isnull(), 'GarageFinish'] = 0
recode_ordinal (data,'GarageFinish',['Unf','RFn','Fin'])
#Garage Qual
data.loc[data ['GarageQual'].isnull(), 'GarageQual'] = 0
recode_ordinal(data,'GarageQual',['Po','Fa','TA','Gd','Ex'])
#Garage Cond
data.loc[data ['GarageCond'].isnull(), 'GarageCond'] = 0
recode_ordinal(data,'GarageCond', ['Po','Fa','TA','Gd','Ex'])
#Paved Drive
recode_ordinal(data,'PavedDrive', ['N','P','Y'])


# drop YearRemod/Add,YearBuilt,GarageYrBlt
data = data.drop(['YearRemod/Add','YearBuilt','GarageYrBlt'],axis=1)

# write to csv file
data.to_csv('train1.csv', index = False)