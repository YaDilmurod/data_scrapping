import subprocess
import time
from datetime import timedelta

def run_python_script(script_path):
    try:
        start_time = time.time()
        subprocess.run(['python', script_path], check=True)
        end_time = time.time()
        execution_time = end_time - start_time
        execution_time_delta = timedelta(seconds=execution_time)
        formatted_time = str(execution_time_delta).split(".")[0]
        print(f"Time {script_path}: {formatted_time}: hh:mm:ss")
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
    
    # print('Data scrapping:')
    # print("\nScript: 1")
    # run_python_script(file1)
    # print("\nScript: 2")
    # run_python_script(file2)
    # print("\nScript: 3")
    # run_python_script(file3)
    # print("\nScript: 4")
    # run_python_script(file4)
    # print("\nScript: 5")
    # run_python_script(file5)

    print('Preprocessing and model:')
    print("\nScript: 1")
    run_python_script(file6)
    print("\nScript: 2")
    run_python_script(file7)
    print("\nScript: 3")
    run_python_script(file8)
