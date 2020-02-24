
import pandas as pd
import numpy as np
census=pd.read_csv('census.csv')
print(census.head())
''' qstn 5 which state has most number of counties'''

state_county=census[['STNAME','CTYNAME','REGION']] #'REGION' added just to experiment
count=state_county.groupby(["STNAME"]).count() #counts under every other column will be same
print(count.head())
print("QSTN 5- {} has most counties".format(count['CTYNAME'].idxmax())) #"CTYNAME" or "REGION" can be used as both are counted and recorded

'''' qstn 6- three most populas counties of each state '''
census1=census.copy()
census1.drop(census1[census1['SUMLEV']==40].index,inplace=True)
pop=census1.copy()
pop=pop[['STNAME','CTYNAME','CENSUS2010POP']]
pop.set_index(['STNAME','CTYNAME'],inplace=True)
pop.sort_values(['STNAME','CENSUS2010POP'],ascending=[True,False],inplace=True) #ascending =False ==>descending
pop=pop.groupby(level=0).head(3)
#very very important to select top values in multiindex df
highest=list(pop.index.get_level_values(level=1)) #used to get index values on a multiindex df
print('QSTN 6- Most 3 populas counties of each state are',highest[:5],'etc.')
''' qstn 7 to find max abs difference in population '''
census7=census.copy()
census7.drop(census7[census7['SUMLEV']==40].index,inplace=True)
census7.drop(['STNAME'],axis=1,inplace=True)
census7.set_index(['CTYNAME'],inplace=True)
max_diff=[]
max_diff_county=[]
columns=['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']
for pop1 in columns:
    for pop2 in columns:
        x=list(abs(i-j) for i,j in zip(census7.loc[:,pop1],census7.loc[:,pop2]))
        max_diff.append(max(x))
        y=x.index(max(x))
        max_diff_county.append(census7.iloc[[y]].index)
maxin=max_diff.index(max(max_diff)) #index position of max value of the list
max_county=max_diff_county[maxin]
print('QSTN 7- County that experienced most change in pop is',max_county[0])
''' Nailed it '''

''' Qstn 8 to find some counties that meet some condition '''
census8=census.copy()
census8=census8[['REGION','STNAME','CTYNAME','POPESTIMATE2014','POPESTIMATE2015']]
mask=((census8['REGION']==1 )|(census8['REGION']==2 )) & (census8['CTYNAME'].str.startswith('Washington')) & (census8['POPESTIMATE2015'] > census8['POPESTIMATE2014'])
#mask=mask & (census8['POPESTIMATE2015'] > census8['POPESTIMATE2014'])
census8= census8[mask]
census8=census8[['STNAME','CTYNAME']]
print('QSTN 8- County satisfying conditions',census8)
