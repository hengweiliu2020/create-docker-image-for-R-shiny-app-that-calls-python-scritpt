#!/usr/bin/python3
import pandas as pd
import numpy as np

df = pd.read_sas('class.sas7bdat')
df2 = df.groupby('trt').describe().unstack(1)
df2 = df2.reset_index()

def summary(my_var, decimal):
    # handle the decimals
    df2.loc[df2['level_1'] == 'count', 'v0'] = df2[0]
    df2.loc[df2['level_1'] == 'mean', 'v0'] = round(df2[0], decimal+1)
    df2.loc[df2['level_1'] == 'std', 'v0'] = round(df2[0], decimal+2)
    df2.loc[df2['level_1'] == 'min', 'v0'] = round(df2[0], decimal)
    df2.loc[df2['level_1'] == 'max', 'v0'] = round(df2[0], decimal)
    df2.loc[df2['level_1'] == '50%', 'v0'] = round(df2[0], decimal+1)

    # get the subsets of required information
    age = df2[
        (df2["level_0"] == my_var) & (df2['level_1'] != 'max') & (df2['level_1'] != '25%') & (df2['level_1'] != '75%')]
    age_max = df2[(df2["level_0"] == my_var) & (df2["level_1"] == 'max')]
    age_max = age_max.rename(columns={'v0': 'max'}).drop(columns=['level_0', 'level_1', 0])

    # do a merge to combine the min, max
    merged = pd.merge(left=age, right=age_max, how='left', left_on='trt', right_on='trt')
    merged['val'] = np.where(merged["level_1"] == 'min', merged['v0'].astype(str) + ',' + merged['max'].astype(str),
                             merged['v0'].astype(str))

    # create a column called statistics
    merged.loc[merged['level_1'] == 'count', 'statistics'] = 'n'
    merged.loc[merged['level_1'] == 'min', 'statistics'] = 'min, max'
    merged.loc[merged['level_1'] == '50%', 'statistics'] = 'median'
    merged.loc[merged['level_1'] == 'mean', 'statistics'] = 'mean'
    merged.loc[merged['level_1'] == 'std', 'statistics'] = 'std'

    # do transpose to get the two treatments in two columns
    age3 = merged[merged['trt'] == b'trt_a']
    age4 = merged[merged['trt'] == b'trt_b']

    age3.rename(columns={'val': 'trt_a'}, inplace=True)
    age4.rename(columns={'val': 'trt_b'}, inplace=True)

    age3 = age3[["statistics", 'trt_a']]
    age4 = age4[["statistics", 'trt_b']]

    # output the final dataset
    merged2 = pd.merge(left=age3, right=age4, how='left', left_on='statistics', right_on='statistics')
    return(merged2)

outdata=summary('Height', 1)

print(outdata)