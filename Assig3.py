import pandas as pd
import numpy as np

''' loading energy =  Energy Indicators.xls'''
energy=pd.read_excel('Energy Indicators.xls',skiprows=17,skipfooter=38,na_values='...')
energy.drop(['Unnamed: 0','Unnamed: 1'],axis=1,inplace=True)
energy.columns=['Country','Energy Supply','Energy Supply per Capita','% Renewable']
energy['Energy Supply']=energy['Energy Supply']*1000000
#energy.set_index('Country1',inplace=True)
energy['Country'].replace({'Republic of Korea':'South Korea','United States of America':'United States','United Kingdom of Great Britain and Northern Ireland':'United Kingdom','China, Hong Kong Special Administrative Region':'Hong Kong'},inplace=True)
#print(energy.head())
'''Function to clean country names'''
def clean(row):
    if row['Country'].isalpha():
        return row
    elif row['Country'].isalnum() or '(' in row['Country']:
        for i in range(len(row['Country'])):
            if row['Country'][i].isdigit() or row['Country'][i]=='(':
                row['Country']=row['Country'][:i]
                #print(row['Country'])
                return row
    else:
        return row

energy=energy.apply(clean,axis=1)

''' loading GDP= World_Bank.csv '''
GDP=pd.read_csv('World_Bank.csv',skiprows=4)
GDP.rename(columns={'Country Name':'Country'},inplace=True)
GDP['Country'].replace({'Korea, Rep.': 'South Korea','Iran, Islamic Rep.':'Iran','Hong Kong SAR, China':'Hong Kong'},inplace=True)
GDP=GDP.apply(clean,axis=1)
#print(GDP.head())

''' loading scimEn = scimagojr-3.xlsx'''
scimEn=pd.read_excel('scimagojr-3.xlsx',headers=0)

merge1=pd.merge(energy,GDP[['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']],how='outer',left_on='Country',right_on='Country')
scimagojr=pd.merge(scimEn.head(15),merge1,how='inner',on='Country')
#print(scimagojr.head())

''' How much had the GDP changed over the 10 year span for the country with 6th largest avg GDP'''
GDP1=scimagojr.copy()
GDP1['Avg GDP']=GDP1[['2006','2007','2008','2009','2010','2011','2012','2013','2015']].apply(np.average,axis=1)
GDP1.sort_values('Avg GDP',ascending=False,inplace=True)
print('The change in GDP for',GDP1['Country'].iloc[5],'(which has the 6th largest avg GDP) =',GDP1['2015'].iloc[5]-GDP1['2006'].iloc[5])

''' Mean of Energy Supply per Capita '''
print('Mean of Energy Supply per Capita = {:.2f}'.format(np.mean(scimagojr["Energy Supply per Capita"])))

''' Counrty with highest amount of % Renewable energy '''
print(scimagojr['Country'].iloc[np.argmax(scimagojr['% Renewable'])], 'has highest amount of % Renewable Energy with',np.max(scimagojr['% Renewable']),'%')

''' creating new column with a ratio and find max of it and return a tuple with country with max and max ratio '''
new=scimagojr.copy()
new['Self:Total Citations']= new['Self-citations']/new['Citations']
#print(new[['Citations','Self-citations','Self:Total Citations']].head())
citmax=(new['Country'].iloc[np.argmax(new['Self:Total Citations'])],'{:.5f}'.format(np.max(new['Self:Total Citations'])))
print('Country with max self:total citations and the max value are',citmax)

''' another operation and corelation finder '''
scimagojr['PopEst']=scimagojr["Energy Supply"]/scimagojr['Energy Supply per Capita']
scimagojr['Citations per Capita']=scimagojr['Citations']/scimagojr['PopEst']
print('corelation',scimagojr[["Energy Supply per Capita",'Citations per Capita']].corr().loc['Citations per Capita','Energy Supply per Capita'])

'''

from matplotlib import pyplot as plt
scimagojr.plot(x='Citations per Capita',y='Energy Supply per Capita',kind='scatter')
plt.show()

'''
''' creating a function and using .apply() '''

def sort_mid(df,med):
    if df['% Renewable'] >= med:
        df['HighRenew']=1
        return df
    else:
        df['HighRenew']=0
        return df

scimagojr=scimagojr.apply(sort_mid,med=scimagojr['% Renewable'].median(),axis=1)
scimagojr.sort_values('Rank',ascending=True)

''' grouping by continents '''
continentdict={'China':'Asia','United States':'North America','Japan':'Asia','United Kingdom':'Europe','Russian Federation':'Europe','Canada':'North America','Germany':'Europe','India':'Asia','France':'Europe','South Korea':'Asia','Italy':'Europe','Spain':'Europe','Iran':'Asia','Australia':'Australia','Brazil':'South America'}
cont=pd.Series(continentdict,name='Continent')
scimagojr=scimagojr.merge(cont.to_frame(),how='inner',left_on='Country',right_index=True) #merging a named series to df. .to_frame() can also be used to convert series to a data frame
scibin=scimagojr.groupby('Continent').agg({'PopEst':[np.size,np.sum,np.mean,np.std]})
#scibin is the required df
#print(scibin.head())

''' putting everything into binn'''
binn=scimagojr[['Country','Continent','% Renewable']].copy()
binn['% Renewable']=pd.cut(binn['% Renewable'],bins=5)
binn.dropna(axis=0,inplace=True)
binn=binn.groupby(['Continent','% Renewable']).count() #columns inside groupby become indices and function is applied upon other columns
binn.dropna(inplace=True)
#print('binnnn')
print(binn.head())
#binn is the required df


''' creating string from a series '''
poplist=scimagojr['PopEst'].values.tolist()
popestimate=','.join('{}'.format(x) for x in poplist)
print(popestimate)

''' changing dtype of column '''
scimagojr['PopEst']=scimagojr['PopEst'].map('{:,}'.format) #map takes an input map it with the argument and return the return value of the function inside
print(scimagojr['PopEst'].head())
scimagojr['PopEst'].astype(str) ##not completed
print(type(scimagojr['PopEst'].values))
