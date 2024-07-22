# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:52:36 2024

@author: cassi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import re

filepath = 'https://data.cdc.gov/api/views/mssc-ksj7/rows.csv?accessType=DOWNLOAD'
filepath2 = 'PLACES__Place_Data__GIS_Friendly_Format___2023_release_20240711.csv'
column_meanings = 'https://www.opendatanetwork.com/dataset/chronicdata.cdc.gov/vgc8-iyc4'
'''more in depth explanations of columns: https://www.cdc.gov/places/measure-definitions/index.html'''

# ingest data from the web and save it in a pandas dataframe for processing and analysis
df = pd.read_csv(filepath2)
print(df.head())

# explore the columns of the dataframe
print(df.columns[0:50])
print(df.columns[50:100])
print(df.columns[100:])

# function to sort columns into the correct category
def categorize(col, pattern):
    for p in pattern:
        if re.search(p, col):
            return True
    return False

# Function to parse string into tuple of floats
def process_ci(item):
    item = str(item)
    item = re.sub(r'[()]', '', item)
    item_tuple = tuple(map(float, item.split(',')))
    return item_tuple

# patterns for confidence intervals
cip = ['_Crude95CI', '_Adj95CI']
        
# patterns for health outcomes
hop = ['ARTHRITIS', 'CANCER', 'BPHIGH', 'CASTHMA', 'CHD', 'COPD', 'DIABETES', 
       'DEPRESSION', 'HIGHCHOL', 'KIDNEY', 'OBESITY', 'STROKE', 'TEETHLOST']

# patterns for health risk behaviors
hrbp = ['BINGE', 'CSMOKING', 'SLEEP', 'LPA']

# patterns for health status 
# (poor general health, poor mental health, poor physical health, self reported)
hsp = ['GHLTH', 'MHLTH', 'PHLTH']

# patterns for disabilities
dp = ['HEARING', 'VISION', 'COGNITION', 'MOBILITY', 'SELFCARE', 'INDEPLIVE', 'DISABILITY']

# patterns for social determinants of health. Not in this dataset?
sdohp = []

# patterns for prevention
pp = ['ACCESS2', 'BPMED', 'CERVICAL', 'CHECKUP', 'CHOLSCREEN', 'COLON_SCREEN', 
      'COREM', 'COREW', 'DENTAL', 'MAMMOUSE']


# sort out the confidence interval columns for processing
ci_col_list = [col for col in df.columns if categorize(col, cip)]
ci_cols = df[ci_col_list]
print(ci_cols.columns)
print(ci_cols.dtypes)
print(ci_cols.head())

# map the to tuple function onto every confidence interval column
ci_cols = ci_cols.map(process_ci)
print(ci_cols['ACCESS2_Crude95CI'][0][1])

# merge the processed confidence interval columns back into the main dataframe
print(df['ACCESS2_Crude95CI'][0][1])
for col, values in df.items():
    if categorize(col, ci_cols.columns.tolist()):
        df[col] = ci_cols[col]
        
print(df['ACCESS2_Crude95CI'][0][1])

#  drop confidence interval columns to directly compare columns.
drop_columns = [col for col in df.columns if categorize(col, cip)]
df_processed = df.drop(drop_columns, axis=1)

# CREATE DATAFRAMES OF ALL THE DIFFERENT CATEGORIES 

# Filter the columns based on the health outcome patterns
matching_columns = [col for col in df_processed.columns if categorize(col, hop)]

# Create the health outcomes categorized dataframe
health_outcomes = df_processed[matching_columns]
print(health_outcomes.columns)
  
matching_columns = [col for col in df_processed.columns if categorize(col, hrbp)]
health_risks = df_processed[matching_columns]   
print(health_risks.columns)

matching_columns = [col for col in df_processed.columns if categorize(col, hsp)]
health_status = df_processed[matching_columns] 

matching_columns = [col for col in df_processed.columns if categorize(col, dp)]
disabilities = df_processed[matching_columns]    

matching_columns = [col for col in df_processed.columns if categorize(col, pp)]
prevention = df_processed[matching_columns]    

# location dataframe
location = df_processed[['StateAbbr', 'StateDesc', 'PlaceName', 'PlaceFIPS', 'TotalPopulation', 'Geolocation']]

categories = {'health_outcomes': health_outcomes,
              'health_risks': health_risks, 
              'health_status': health_status, 
              'disabilities': disabilities, 
              'prevention': prevention, 
              'location': location
              }

# bar chart of the prevalence of binge drinking by location 
drink_loc = df[['BINGE_AdjPrev', 'StateDesc', 'PlaceName']]
dlt = drink_loc.groupby('StateDesc').agg({'BINGE_AdjPrev': ['min', 'max', 'mean']})
dlt_sorted = dlt.sort_values(('BINGE_AdjPrev', 'mean'), ascending=False)
print(dlt_sorted)
bar = dlt_sorted.plot(kind='bar', figsize=(15,7))
bar.legend(title='Legend', labels=['min', 'max','mean'])
plt.ylabel('Age Adjusted prevalence of Binge Drinking (%)')
plt.xlabel('State')
plt.title('Minimum, Maximum, and Average Prevalence of Binge Drinking by State')
plt.show()

# scatterplot of binge drinking related to depression
x = df['BINGE_AdjPrev']
y = df['DEPRESSION_AdjPrev']
plt.figure(figsize=(15,7))
scatter = plt.scatter(x, y, c=pd.Categorical(location['StateAbbr']).codes, cmap='tab20')
cbar = plt.colorbar(scatter)
cbar.set_ticks(range(len(location['StateAbbr'].unique())))
cbar.set_ticklabels(location['StateAbbr'].unique())
plt.xlabel('Age Adjusted Prevalence of Binge Drinking (%)')
plt.ylabel('Age Adjusted Prevalence of Depression (%)')
plt.title('Depression and Binge Drinking by State')
plt.show()

# function to identify columns pairs (crude and age adjusted columns refering to same variable)
def identify_exclude_pairs(columns):
    exclude_pairs = []
    crude_pattern = re.compile(r'_CrudePrev$')
    adj_pattern = re.compile(r'_AdjPrev$')
    for col in columns:
        if crude_pattern.search(col):
            base_name = crude_pattern.sub('', col)
            adj_col = base_name + '_AdjPrev'
            if adj_col in columns:
                exclude_pairs.append((col, adj_col))
    return exclude_pairs

# function to filter and sort correlation matrices
def filter_sort_corr_matrix(corr_matrix, threshold, exclude_pairs):
    filtered_corr_matrix = corr_matrix.where(corr_matrix.abs() >= threshold)
    # for identified paired columns, set their correlation to NaN to filter out
    for pair in exclude_pairs:
        filtered_corr_matrix.at[pair[0], pair[1]] = np.nan
        filtered_corr_matrix.at[pair[1], pair[0]] = np.nan
    # convert to series, drop na values and sort
    corr_pairs = filtered_corr_matrix.unstack().dropna().sort_values(ascending=False)
    return corr_pairs[corr_pairs < 1] # remove self correlation


# correlate within groups
internal_matrix_list = []
for key, value in categories.items():
    #print(key, value)
    #drop non-numeric columns
    num_df = value.select_dtypes(include=[np.number])
    # find column pairs to exclude
    exclude_pairs = identify_exclude_pairs(num_df.columns)
    # calculate correlations
    corr_matrix = num_df.corr()
    # filter and sort correlations
    filtered_corr = filter_sort_corr_matrix(corr_matrix, 0.5, exclude_pairs)
    
    internal_matrix_list.append({'name': key, 'correlation_matrix': filtered_corr})
    
for item in internal_matrix_list:
    print(f"Category: {item['name']}")
    print(item['correlation_matrix'])
    print('\n')

# correlate the different groups with each other
num_processed_df = df_processed.select_dtypes(include=[np.number])
exclude_pairs = identify_exclude_pairs(num_processed_df.columns)
external_corr_matrix = filter_sort_corr_matrix(num_processed_df.corr(), 0.5, exclude_pairs)

print('sorted correlations between categories:')
print(external_corr_matrix)
print('correlation to binge drinking')
print(external_corr_matrix['BINGE_AdjPrev'])


# FUTURE WORK: Use KNN algorithm to predict future prevalence of health outcomes based on health risks/binge drinking

print('finished')

'''
The data pipeline
Ingest Data
1.	Ingest data into the program through the URL.
Store Data
2.	Store the data in a pandas dataframe.
Process Data
3.	Convert the confidence interval columns from a string format to a tuple format to use in analysis.
4.	Create a new dataframe that does not include the confidence interval columns to directly compare prevalence columns.
5.	Separate remaining columns into categories defined by the CDC: health outcomes, health risks, health status, disabilities, prevention, and location. 
6.	Remove non-numerical data when comparing columns.
7.	Remove comparisons between column pairs of crude and age-adjusted values.
Analyze Data
8.	Visualize some of the data in a table and bar chart, grouped by state and organize in descending order.
9.	Visualize data in a scatterplot comparing two columns and coloring by state.
10.	Find columns with high correlations to each other within each category using correlation matrices.
11.	Find columns with high correlations to each other between categories using a correlation matrix.

Applications of Program
•	This framework is applicable to any data that contains confidence intervals and has sub-categories
•	The pattern recognition function could help sort data by keywords, such as symptoms, causes, outcomes, etc.
•	Any column could be entered into the visualization code to see trends
•	The correlation matrices allow the user to pick out the columns most correlated to each other for further analysis, 
which is useful for any dataset where relationships between variables is of interest (causes and impacts of climate change, 
outcomes of policy decisions, outcomes of cancer treatments, etc.)
•	This is a descriptive analysis program, but trends seen here could be used to build predictive analysis. For example,  
using the k-nearest neighbors algorithm to predict health outcomes based on prevention and health risks.

'''