# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import hungarian as hg

team = pd.read_csv("team_draft.csv", encoding="utf-8")

def penalty(series):
    series.ix[:,0:6] = series.ix[:,0:6].replace([0],-1)
    series['Score'] = series['Group 2']*5 + series['Group 3']*4 + series['Group 4']*3 + series['Group 5']*2 + series['Phone']*1
    series = series.sort_values(by='Score')
    series.index = range(0,len(series))
    return series
    
team = penalty(team)

#slicing and segmentation of data
dgroup = np.array(team.ix[:,0:7]) #district names, groups
dgroup_headers = team.columns.values[0:7] #column headers for dgroup
team_names = team.columns.values[8:17] #column headers for team ranks
vlowscore_array = np.array(team.ix[:2,8:18], dtype='f') #districts 1-3 based on low score
highscore_array = np.array(team.ix[21:,8:18], dtype='f')
midscore_array = np.array(team.ix[12:20,8:18], dtype='f')
lowscore_array = np.array(team.ix[3:11,8:18], dtype='f')
costmatrices = {
                range(21,30):highscore_array,
                range(12,21):midscore_array, 
                range(3,12):lowscore_array,
                range(0,3):vlowscore_array 
                }

#assignment using hungarian 
hg_results=[]
for i in costmatrices:
    hungarian = hg.Hungarian()
    hungarian.calculate(costmatrices[i])
    result = hungarian.get_results()
    result.sort()
    hg_results.append(pd.DataFrame({'Results':result},
                                index = [x for x in i]))

re = pd.concat(hg_results)
re.ix[0:2,'Results'] = 'None'
t = [team, re]
team = pd.concat(t, axis=1)

#creating results table
results = pd.DataFrame(dgroup, columns=dgroup_headers)
results['Draft Results'] = 0
results['Team Pick Number'] = 0
for i in range(len(re.ix[0:2]),len(re)):
    try:
        results['Draft Results'][i] = team_names[re['Results'][i][1]]
        results['Team Pick Number'][i] = team[team_names[re['Results'][i][1]]][i]
    except TypeError:
        pass
results = results.replace([-1],0)
try:
    results = results.sort_values(by='Draft Results')
except TypeError:
    pass

#write function to take series, find min value, assign to parent DF, recalculate min value
    
drafttotal = results.groupby('Draft Results')['Dealer Total'].sum()
drafttotal = drafttotal.drop(drafttotal.index[drafttotal.index.isin([0])==True])
drafttotal = drafttotal.sort_values(ascending=False)
for i in range(1,4):
    results['Draft Results'][i-1]= drafttotal.index[i-4]
drafttotal2 = results.groupby('Draft Results')['Dealer Total'].sum()
drafttotal2.sort()

results.index = range(0,len(results))
results.to_csv('team-draft.csv', headers='Yes', index='No')
team.to_csv('penalty-draft.csv', headers='Yes', index='No')

#optimization
'''
drafttotal = results.groupby('Draft Results')['Dealer Total'].sum()
drafttotal = drafttotal.drop(drafttotal.index[drafttotal.index.isin([0])==True])
drafttotal.sort()
for i in range(0,len(drafttotal.ix[:3])):
    results['Draft Results'][i]= drafttotal.index[i]'''
        
    

#secondary team assignment

