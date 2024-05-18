# Define the file name
file_name = "dags/txt.txt"

# Define the file content
file_content = "This is me"

# Create the text file
with open(file_name, 'w') as file:
    file.write(file_content)

print(f"Text file '{file_name}' created successfully.")
