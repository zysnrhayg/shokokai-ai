# Load SQL statement from file
def read_sql_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
