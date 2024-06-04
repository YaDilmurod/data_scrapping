# %%
import pandas as pd
from datetime import datetime

# %%
# Replace 'your_file.xlsx' with the correct path to your Excel file
excel_file_path = '/Users/didi/Desktop/data_scrapping/Data Scrapping/Data/Local Excel/cenovaya_setka_jiloy.xlsx'

# Read Excel file into a DataFrame
jiloy = pd.read_excel(excel_file_path)


# %%
russian_column_names = {
    'views': 'Просмотры',
    'floor': 'Этаж',
    'szhil': 'Площадь',
    'skitchen': 'Площадь кухни',
    'roof_heigh': 'Высота потолков',
    'plan': 'Планировка',
    'sanuzel': 'Санузел',
    'balcon': 'Балкон',
    'type_remon': 'Тип ремонта',
    'series': 'Серия дома',
    'data_end': 'Дата завершения',
    'infrastr': 'Инфраструктура',
    'type_build': 'Тип строения',
    'rooms': 'Количество комнат',
    'vtor_perv': 'Вторичка/первичка',
    'source_id': 'Идентификатор источника',
    'source_url': 'URL источника',
    'source_dat': 'Дата источника',
    'price_mete': 'Цена за метр',
    'price_sot': 'Цена за сотку',
    'price_obje': 'Цена',
    'appointmen': 'Назначение',
    'type': 'type',
    'etaj': 'Этажность',
    'dop_k_domu': 'Дополнения к дому',
    'sotki_ijs': 'Сотки или кв. м',
    'actual_dat': 'Дата публикации',
    'source_nam': 'Источник',
    'xcoord': 'Долгота',
    'ycoord': 'Широта',
    'district': 'Район',
    'operator': 'Оператор'
}

# Assuming your DataFrame is named 'jiloy'
jiloy['Название'] = jiloy['opisanie1'].astype(str) + ' ' + jiloy['opisanie2'].astype(str)

# Drop the original columns if needed
jiloy = jiloy.drop(['opisanie1', 'opisanie2'], axis=1)
jiloy['actual_dat'] = pd.to_datetime(jiloy['actual_dat']).dt.strftime('%d-%m-%Y')
jiloy['actual_dat'] = pd.to_datetime(jiloy['actual_dat'], format='%d-%m-%Y').dt.strftime('%d.%m.%Y')

jiloy = jiloy[jiloy['type'].str.lower() != 'аренда']

jiloy = jiloy.rename(columns=russian_column_names)
final_df = jiloy.drop(['id', 'Просмотры', 'Высота потолков', 'Балкон', 'Дополнения к дому', 'Оператор', 'Инфраструктура'],  axis=1)
pd.set_option('display.max_columns', None)


# %%
column_name_mapping = {
    "Назначение": "Тип",
    "Вторичка/первичка": "Тип постройки",
    "Тип ремонта": "Ремонт", 
    "Тип строения": "Материал",
}

# Rename the columns
final_df.rename(columns=column_name_mapping, inplace=True)


# %%
columns_to_check = ["Источник", "Название", "Тип","Санузел", "Тип постройки", "Материал", "Широта", 
                    "Долгота", "Район", "Этаж", "Этажность", "Ремонт", "Площадь", 
                    "Количество комнат", "Дата публикации", "Валюта", "Цена", "Дата создания"]

# Create a new DataFrame with the specified columns
new_df = pd.DataFrame(columns=columns_to_check)

# Check if columns exist in final_df and create them with None values if not
for column in columns_to_check:
    if column not in final_df.columns:
        final_df[column] = None
        new_df[column] = None
    else:
        new_df[column] = final_df[column]
        
new_df["Источник"] = 'Local'
new_df["Валюта"] = 'USD'
new_df["Район"] = ''
new_df["Дата создания"] = datetime.now().strftime("%d.%m.%Y")
new_df[columns_to_check]
new_df.head()



# %%
# Specify columns to check for duplicates
columns_to_check_dup = ["Источник", "Название", "Тип", "Санузел", "Тип постройки", "Материал", 
                    "Широта", "Долгота", "Район", "Этаж", "Этажность", "Ремонт", "Площадь", 
                    "Количество комнат", "Дата публикации", "Валюта", "Цена"]

# Count the number of rows before removing duplicates
rows_before = new_df.shape[0]

# Remove duplicates based on specified columns
df_no_duplicates = new_df.drop_duplicates(subset=columns_to_check_dup, keep=False)

# Count the number of rows after removing duplicates
rows_after = df_no_duplicates.shape[0]

# Calculate the number of rows deleted
rows_deleted = rows_before - rows_after

print(f"\nNumber of rows deleted: {rows_deleted}")


# %%
# %%
import pandas as pd
import os

df = pd.DataFrame(new_df)

excel_file_name = 'Data Scrapping/Excels/Local/Local.xlsx'

# Check if the file already exists
if os.path.exists(excel_file_name):
    # Read the existing Excel file into a DataFrame
    existing_df = pd.read_excel(excel_file_name)

    # Append the new data to the existing DataFrame
    updated_df = pd.concat([existing_df, df], ignore_index=True)

    # Check for duplicates in all columns
    duplicates_mask = updated_df.duplicated(keep=False)

    # Print the number of duplicates
    num_duplicates = duplicates_mask.sum()
    print(f"Number of duplicates after adding new data: {num_duplicates}")

    # If duplicates exist, remove them
    if any(duplicates_mask):
        updated_df = updated_df[~duplicates_mask]

    # Write the updated DataFrame back to the Excel file
    updated_df.to_excel(excel_file_name, index=False)

    print(f"Data added to existing Excel file '{excel_file_name}' after removing duplicates.")
else:
    # If the file doesn't exist, create a new Excel file with the data
    df.to_excel(excel_file_name, index=False)
    print(f"Excel file '{excel_file_name}' created with new data.")

