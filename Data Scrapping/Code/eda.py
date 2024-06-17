# %%
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np


# %%
data = pd.read_excel("Data Scrapping/Data/Combined.xlsx")

df = pd.DataFrame(data)
df = df[df['Цена'] != 0]
df.shape


# %%
column_translation = {
    'Источник': 'source',
    'Название': 'title',
    'Тип': 'type',
    'Санузел': 'bathroom',
    'Тип постройки': 'building_type',
    'Материал': 'material',
    'Широта': 'lat',
    'Долгота': 'long',
    'Район': 'district',
    'Этаж': 'floor',
    'Этажность': 'num_of_floors',
    'Ремонт': 'renovation',
    'Площадь': 'area',
    'Количество комнат': 'num_of_rooms',
    'Дата публикации': 'publication_date',
    'Валюта': 'currency',
    'Цена': 'price',
    'Дата создания': 'created_date'
}

df = df.rename(columns=column_translation)

df = df[['source', 'type', 'building_type',
       'lat', 'long', 'district', 'floor', 'num_of_floors', 'renovation',
       'area', 'num_of_rooms', 'publication_date', 'currency', 'price']]


# %%
init_len = len(df)

subset_columns = ['type', 'building_type', 'district', 'floor', 'num_of_floors', 'renovation',
         'area', 'num_of_rooms']

df = df.drop_duplicates(subset=subset_columns)

after_len = len(df)
print("Number of duplicates removed:", init_len - after_len)


# %%
usd_mask = df['currency'] == "USD"
df.loc[usd_mask, 'price'] *= 12500
df.loc[usd_mask, 'currency'] = "UZS"


# %%
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d.%m.%Y')
df['year'] = df['publication_date'].dt.year
df['year'] = df['year'].fillna(np.nan).astype(float).astype('Int64')


# %%
df = df[['source', 'type', 'building_type',
       'lat', 'long', 'district', 'floor', 'num_of_floors', 'renovation',
       'area', 'num_of_rooms', 'currency', 'price', 'year']]

# %%
district_borders = gpd.read_file('Data Scrapping/Data/district_borders.json')
df['geometry'] = df.apply(lambda row: Point(row['long'], row['lat']), axis=1)
gdf = gpd.GeoDataFrame(df, geometry='geometry')
joined = gpd.sjoin(gdf, district_borders, how="left", op='within')
df['district'] = df['district'].fillna(joined['NOMI'])
df.drop(columns=['geometry'], inplace=True)


# %%
df['type'] = df['type'].str.lower()

corrections = {
    'квартира': 'apartment',
    'квартира': 'apartment',
    'частный дом': 'house',
    'земля': 'house',
    'участок': 'house',
    'евро дом': 'house',
    'дом': 'house',
    'частный дом на продажу':'house',
    'квартира во вторичке на продажу': 'apartment',
    'квартира в новостройке на продажу': 'apartment',
    'дача на продажу': 'house',
}                                       

df['type'].replace(corrections, inplace=True)

allowed_categories = corrections.values()
df = df[df['type'].isin(allowed_categories)]
df.reset_index(drop=True, inplace=True)


# %%
df['building_type'] = df['building_type'].str.lower()

corrections = {
    'Новострой': 'Primary market',
    'Вторичный': 'Secondary market',
    'Вторичка': 'Secondary market',
    'Вторичный рынок': 'Secondary market',
    'Новостройки': 'Primary market',
    'Первичный': 'Primary market',
    'вторичный': 'Secondary market',
    'Новостройка': 'Primary market',
    'первичный': 'Primary market',
    'первычный': 'Primary market',
    'Вторичний':  'Secondary market',
    'торичный': 'Secondary market',
    'Вторичные': 'Secondary market',
    'Вторичный': 'Secondary market',
    'вторичный рынок': 'Secondary market',
    'новостройка': 'Primary market',
    'новостройки': 'Primary market',
    'новострой': 'Primary market',
    'вторичка': 'Secondary market',
}

df['building_type'].replace(corrections, inplace=True)
allowed_categories = corrections.values()
df = df[df['building_type'].isin(allowed_categories)]
df.reset_index(drop=True, inplace=True)


# %%
df['renovation'] = df['renovation'].str.lower()

corrections = {
    'евро ремонт': 'Euro',
    'квро ремонт': 'Euro',
    'евро ремонт': 'Euro',
    'с ремонтом': 'Normal',
    'требуется ремонт': 'Required',
    'требует ремонта': 'Required',
    'средняя': 'Normal',
    'среднее состояние': 'Normal',
    'требует ремонта': 'Required',
    'незаконченный евроремонт': 'Required',
    'требует ремонта':  'Required',
    'дизайнерский': 'Euro',
    'не требуется': 'Normal',
    'косметический': 'Euro',
    'черновая отделка': 'Required',
    'коробка': 'Required',
    'без ремонта': 'Required',
    'капитальный ремонт': 'Euro',
}

df['renovation'].replace(corrections, inplace=True)
allowed_categories = corrections.values()
df = df[df['renovation'].isin(allowed_categories)]
df.reset_index(drop=True, inplace=True)

# %%
for column in df.columns:
    mode_value = df[column].mode()[0]
    df[column] = df[column].fillna(mode_value)


# %%
def remove_outliers(df, column, threshold):
    # Convert column to numeric type if necessary
    df[column] = pd.to_numeric(df[column], errors='coerce')
    
    # Calculate mean and standard deviation
    mean_val = df[column].mean()
    std_val = df[column].std()
    
    # Calculate lower and upper bounds for outliers
    lower_bound = mean_val - threshold * std_val
    upper_bound = mean_val + threshold * std_val
    
    # Remove outliers
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    
    return df


df = remove_outliers(df, 'price', 1.75)
df = remove_outliers(df, 'num_of_rooms', 1.75)
df = remove_outliers(df, 'area', 1.75)

# df.reset_index(drop=True, inplace=True)

# %%
df = df[['source', 'renovation',	'district', 'area',	'num_of_rooms', 'type', 'building_type', 'price']]

# %%
def encode_and_drop(df, column_name):
    one_hot_encoded = pd.get_dummies(df[column_name], prefix=column_name)
    one_hot_encoded = one_hot_encoded.astype(int)
    
    df = pd.concat([df, one_hot_encoded], axis=1)
    
    df.drop(column_name, axis=1, inplace=True)
    
    return df

columns_to_process = ['district', 'renovation', 'type', 'building_type']
for column in columns_to_process:
    df = encode_and_drop(df, column)

# %%
df.columns

# %%
import os

excel_file_path = "Data Scrapping/Data/Cleaned_Combined.xlsx"
if os.path.exists(excel_file_path):
    existing_data = pd.read_excel(excel_file_path)
    combined_data = pd.concat([existing_data, df])
    combined_data.drop_duplicates(keep='first', inplace=True)
    combined_data.to_excel(excel_file_path, index=False)
else:
    df.to_excel(excel_file_path, index=False)
