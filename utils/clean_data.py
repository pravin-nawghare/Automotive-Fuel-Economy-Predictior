import numpy as np
import pandas as pd


rename_maps = {'vw':'volkswagen', 'chevy':'chevrolet', 'vokswagen':'volkswagen', 'maxda':'mazda','toyouta':'toyota', 'chevroelt':'chevrolet'}

# clean the data
def clean_data(df,column):
    df[column] = df[column].replace('?',np.nan)
    df[column] = df[column].astype(float)
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)
    return df

# remove car names with frequency less than cutoff
def car_name_reduce(categories,cutoff=3):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "other"
    return categorical_map

# clean brand names 
def extract_car_brand(df, old_column, new_column, rename_map):
    df[new_column] =  df[old_column].astype(str).str.split().str[0]

    # rename car names
    if rename_map:
        df[new_column] = df[new_column].map(lambda x: rename_map.get(x,x))
    return df

# convert weight feature into categorical feature
def grouping_car_by_weights(df, column):
    labels = ['1500 - 2000','2000 - 2500','2500 - 3000','3000 - 3500','3500 - 4000','4000 - 4500','up-to 5000']
    bins = [1500,2000,2500,3000,3500,4000,4500, 5000]
    df['weight groups'] = pd.cut(df[column], bins=bins, labels=labels)
    return df

# start data pre-processing
def load_data():
    df = pd.read_csv('data/raw-auto-mpg.csv')
    #clean data
    df = clean_data(df,'horsepower')
    # extract car brands
    df = extract_car_brand(df, 'car name', 'car brand', rename_maps)
    # reduce car name
    car_map = car_name_reduce(df['car name'].value_counts(),4)
    df['car_name'] = df['car name'].map(car_map)
    # group by their weights
    df = grouping_car_by_weights(df, 'weight')
    return df

# load raw data
df = load_data()
# save clean data
df.to_csv("D:/Data-Sorting/fuel_economy/data/auto-mpg.csv",index=False)