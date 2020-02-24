import pandas as pd
import numpy as np
olp=pd.read_csv('olympics.csv',skiprows=1,index_col=0)
''' cleaning the data '''
for col in olp.columns:
    if col.startswith('01'):
        olp.rename(columns={col:'Gold'+col[4:]},inplace=True)
    if col.startswith('02'):
        olp.rename(columns={col:'Silver'+col[4:]},inplace=True)
    if col.startswith('03'):
        olp.rename(columns={col:'Bronze'+col[4:]},inplace=True)
    if col.startswith('№'):
        olp.rename(columns={col:'#'+col[1:]},inplace=True)
names=olp.index.str.split('\(')
olp.index=names.str[0] #I guess .str enables us to consider indices as strings and hence enabling split and slicing
olp['code']=names.str[1].str[:3] #.str can be used inside a list of lists to slice and the output is a list
#print(olp.head())
olp=olp.drop('Totals')
#print(olp.tail())
ad=olp.drop('code',axis=1) #axis 0 is row wise and axis 1 is column wise. Here drop will search for 'code' along column names
#print(ad.head())
#olp['country']=olp.index
#olp.set_index(['code','country'],inplace=True)
#print(olp.head())
#ad=olp.loc['AFG':'ARM']
#print(ad.head())
print(olp.head())
''' retaining only required columns'''
col=['# Summer','Gold','# Winter','Gold.1']
ad=olp[col]
print(ad.head())
''' qstn 2 to find max difference country'''
x=list(map(abs,olp['Gold.1'].sub(olp['Gold'],axis=0))) #oneway to subtract a column from a column
a=x.index(max(x))
print(olp.iloc[[a]])
''' qstn 3 to find the % best '''
x=list((abs(olp['Gold']-olp['Gold.1'])/(sum(olp['Gold'])+sum(olp['Gold.1']))))
print("{0:.2f}".format((x[x.index(max(x))]*100))) #"{0:.2f},{1:4f}".format(number1,number2) is a good way to format and print
''' qstn 4 to create a function to find the points of the country '''
def points(df):
    pnt=pd.Series(name='Point')
    for cntry in df.index:
        pnt[cntry]=df.loc[cntry,'Gold.2']*3 + df.loc[cntry,'Silver.2']*2 + df.loc[cntry,'Bronze.2']*1
    return pnt
#pnts=points(olp)
#print(pnts.head())
#print(len(pnts))
''' qstn 1 to find max along a column '''
a=olp['Gold'].idxmax(axis=0,skipna=True) #.idxmax() gives index of the max
print(a)
