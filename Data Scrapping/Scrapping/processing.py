import subprocess
import time

notebooks = ['02.Dom_uz.ipynb', '03.Joymee.ipynb', '05.Olx.ipynb', '06.Uybor.ipynb',
             '01.Grouping_Sources.ipynb', '0001.EDA.ipynb', '00001.LinearRegression.ipynb']

max_retries = 3

for notebook in notebooks:
    retry_count = 0
    while retry_count < max_retries:
        try:
            subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', notebook], check=True)
            break 
        except subprocess.CalledProcessError:
            retry_count += 1
            print(f"Error executing {notebook}. Retrying ({retry_count}/{max_retries})...")
            time.sleep(10) 

    if retry_count == max_retries:
        print(f"Failed to execute {notebook} after {max_retries} retries.")
 