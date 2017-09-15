# Data processing and feature engineering

# Initialise
import pandas as pd

# Read data
train = pd.read_csv('train.csv')

# Convert MsSubClass from float to object
train['MSSubClass'] = train['MSSubClass'].astype(object)

# Convert MoSold from integer to object
train['MoSold'] = train['MoSold'].astype(object)

# Houses with no lot frontage, value is set to 0
train.loc[train['LotFrontage'].isnull(), 'LotFrontage'] = 0

# Houses with missing values for MasVnrType assumed equal to None; area equal 0
train.loc[train['MasVnrType'].isnull(), 'MasVnrArea'] = 0
train.loc[train['MasVnrType'].isnull(), 'MasVnrType'] = 'None'

# Convert all nominal variables to dummy variables (either 0 or 1)
train['CentralAir'] = (train['CentralAir'] == 'Y').astype(int)
nominal = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LandContour', 'LotConfig', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'Foundation', 'Heating', 'GarageType', 'MiscFeature', 'SaleType', 'MoSold']
dummies = pd.get_dummies(train[nominal])

# Join dummy variables to training set and remove original columns
train = train.join(dummies).drop(nominal, axis = 1)

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
recode_ordinal(train, 'LotShape', ['IR3', 'IR2', 'IR1', 'Reg'])
recode_ordinal(train, 'Utilities', ['ELO', 'NoSewa', 'NoSewr', 'AllPub'])
recode_ordinal(train, 'LandSlope', ['Sev', 'Mod', 'Gtl'])
recode_ordinal(train, 'ExterQual', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
recode_ordinal(train, 'ExterCond', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
train.loc[train['BsmtQual'].isnull(), 'BsmtQual'] = 0
recode_ordinal(train, 'BsmtQual', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
train.loc[train['BsmtCond'].isnull(), 'BsmtCond'] = 0
recode_ordinal(train, 'BsmtCond', ['Po', 'Fa', 'TA', 'Gd', 'Ex'])
train.loc[train['BsmtExposure'].isnull(), 'BsmtExposure'] = 0
recode_ordinal(train, 'BsmtExposure', ['No', 'Mn', 'Av', 'Gd'])
train.loc[train['BsmtFinType1'].isnull(), 'BsmtFinType1'] = 0
recode_ordinal(train, 'BsmtFinType1', ['Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'])
train.loc[train['BsmtFinType2'].isnull(), 'BsmtFinType2'] = 0
recode_ordinal(train, 'BsmtFinType2', ['Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'])

# credit to Zhehao Zhang for all lines below
#get the age of House
train['Age_House'] = train ['YrSold'] - train ['YearBuilt']
#whether a house had been reconstructed  
train ['Reconstructed'] = train ['YearRemod/Add'] - train ['YearBuilt']
# 1- the house had been reconstructed, otherwise 0 
train.loc[train ['Reconstructed'] > 0, 'Reconstructed'] = 1 
 
#get the age of Garage
train ['Age_Garage'] = train ['YrSold'] - train ['GarageYrBlt']

####oridnal data
def recode_ordinal (data, colName, levels):
     i = 1
     for lvl in levels:
          data.loc[data[colName] == lvl, colName] = i
          i = i + 1
     data[colName] = data [colName].astype(int)
  # HeatingQC
recode_ordinal (train, 'HeatingQC', ['Po','Fa','TA','Gd','Ex'])   
 #Electrical
recode_ordinal (train, 'Electrical', ['Mix','FuseP','FuseF','FuseA','SBrkr'])
 #KitchenQual
recode_ordinal (train,'KitchenQual', ['Po','Fa','TA','Gd','Ex'])
 #Functional
recode_ordinal (train, 'Functional' , ['Sal','Sev','Maj2','Maj1','Mod','Min2','Min1','Typ'])
 #FireplaceQu
train.loc[train ['FireplaceQu'].isnull(), 'FireplaceQu'] = 0
recode_ordinal(train,'FireplaceQu', ['Po','Fa','TA','Gd','Ex'])
 #Garage Finish
train.loc[train ['GarageFinish'].isnull(), 'GarageFinish'] = 0
recode_ordinal (train,'GarageFinish',['Unf','RFn','Fin'])
 #Garage Qual
train.loc[train ['GarageQual'].isnull(), 'GarageQual'] = 0
recode_ordinal(train,'GarageQual',['Po','Fa','TA','Gd','Ex'])
 #Garage Cond
train.loc[train ['GarageCond'].isnull(), 'GarageCond'] = 0
recode_ordinal(train,'GarageCond', ['Po','Fa','TA','Gd','Ex'])
 
 #Paved Drive
recode_ordinal(train,'PavedDrive', ['N','P','Y'])
 #Pool QC
train.loc[train ['PoolQC'].isnull(), 'PoolQC'] = 0
recode_ordinal(train,'PoolQC', ['Fa','TA','Gd','Ex'])
 #Fence
train.loc[train ['Fence'].isnull(), 'Fence'] = 0
recode_ordinal(train,'Fence', ['MnWw','GdWo','MnPrv','GdPrv'])

#drop  YearRemod/Add,YearBuilt,GarageYrBlt
train.drop (['YearRemod/Add','YearBuilt','GarageYrBlt'],axis=1)
