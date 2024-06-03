import subprocess
import time
from datetime import timedelta

def run_python_script(script_path):
    try:
        start_time = time.time()
        subprocess.run(['python', script_path], check=True)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_minutes = elapsed_time / 60
        print(f"Time taken: {elapsed_time_minutes:.2f} minutes")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file1 = "Data Scrapping/Code/Scrapping/uybor.py"
    file2 = "Data Scrapping/Code/Scrapping/joymee.py"
    file3 = "Data Scrapping/Code/Scrapping/olx.py"
    file4 = "Data Scrapping/Code/Scrapping/dom_uz.py"
    file5 = "Data Scrapping/Code/Scrapping/local.py"

    file6 = "Data Scrapping/Code/Scrapping/grouping_sources.py"
    file7 = "Data Scrapping/Code/eda.py"
    file8 = "Data Scrapping/Code/ml_model.py"

    print('\n-----------')
    print('Data scrapping:')
    print("Script: 1. uybor")
    run_python_script(file1)
    print("\nScript: 2. joymee")
    run_python_script(file2)
    print("\nScript: 3. olx")
    run_python_script(file3)
    print("\nScript: 4. dom_uz")
    run_python_script(file4)
    print("\nScript: 5. local")
    run_python_script(file5)
    print('-----------')

    print('\n-----------')   
    print('Preprocessing and model:')
    print("Script: 1. grouping_sources")
    run_python_script(file6)
    print("\nScript: 2. eda")
    run_python_script(file7)
    # print("\nScript: 3. ml_model")
    # run_python_script(file8)
    print('-----------')
    print('Finished!')
