import glob
import os
import shutil
import yaml
import camelot
import pandas as pd
import numpy as np

def load_yaml(file, template=None):
    """
    Loads a YAML file with error handling and template control.

    Parameters:
        file (str): File path of file to load
        template (str): Optional. File path of template file if original file doesn't exist.

    """
    if template:
        if not os.path.exists(file):
            try:
                shutil.copy(template, file)
                print('File missing. A new one has been created. You must open the new file and define the variables.')
            except FileNotFoundError:
                print('Specified template file does not exist.')
            exit()
    try:
        with open(file, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        print('File not found. Please check path.')
        exit()

def get_files(file_location):
    """
    Returns a list of files from a folder.

    Parameters:
        file_location (str): Folder location of files. Asterisk(*) must be included after folder path to return file paths. 
    """
    print('Getting file(s)...')
    return glob.glob(file_location)

def extract_and_export_tables(file, pages, export_folders, extract_date=False, flavor='stream'):
    """
    Extracts tables from a PDF file and exports them to CSV. Also returns a list of the locations of resulting CSVs.

    Parameters:
        file (str): PDF file to be used. Include full path.
        pages (str): Pages where tables are to be extracted. As string, separated by comma.
        export_folders (str or list): Export location for tables. Input as list.
        extract_date (bool): Extract dates that are at the end of a file. Only works if string is in YYMM format.
        flavor (str): From camelot. 'stream': infers tables. 'lattice': work when tables are clearly defined in PDF.
    """
    csv_paths = []

    if isinstance(export_folders, str):
        export_folders = [export_folders]

    if isinstance(pages, int):
        pages = str(pages)

    file_name = os.path.basename(file)
    print(f'Extracting and exporting tables from {file_name} to csv...')

    try:
        tables = camelot.read_pdf(file, flavor=flavor, pages=pages, suppress_stdout=True)
    except IndexError:
        print('Pages not found. Did you input the correct page numbers?')
        exit()

    if len(export_folders) > 1 and len(tables) != len(export_folders):
        raise ValueError('The number of export folders must match the number of tables extracted when more than one folder is provided.')

    for i, table in enumerate(tables):
        if len(export_folders) == 1:
            folder = export_folders[0]
        else:
            folder = export_folders[i]

        folder_name = os.path.basename(os.path.normpath(folder)).lower().replace(' ', '_')
        if extract_date:
            date_extract = file[-8:-4]
            file_path = os.path.join(folder, f'{folder_name}{date_extract}.csv')
        else:
            file_path = os.path.join(folder, f'{folder_name}.csv')

        table.to_csv(file_path)

        csv_paths.append(file_path)
    
    return csv_paths

# to find location of specific text in dataframe
def find_loc(df, search_value):
    result = np.where(df.apply(lambda row: row.astype(str) == search_value).values)
    locations = list(zip(result[0], result[1]))
    return locations[0][0]

def clean_csv(file, clean_start=None, clean_end=None, filter_column=None, filter_values=[]):
    """
    Performs basic 'cleaning' on a CSV file.

    Parameters:
        file (str or list): CSV(s) to be cleaned. Include full path.
        clean_start (str): Text where you would want column headers to start. If extracted PDF has space or additional unneeded text before data starts, use this option to remove it.
        clean_end (str): Text where you would want data to end. Useful if there is summary columns or unneeded text after data that gets brought in with extraction.
        filter_column (str): Column where you want the filtering to take place.
        filter_values (list): Values to filter out of data. Ex) Filter filter_column where value is in filter_values.
    """
    cleaning_failure_message = (
        'column name in configuration not found. Did you set a name and did you spell it right? Did you mean to run the cleaning function?'
        'Note that while the CSVs exported, due to this failure they were NOT cleaned.'
        'Please check the configuration file and run the script again to clean CSVs.'
    )

    if isinstance(file, str):
        file = [file]

    for csv in file:
        print(f'Cleaning {os.path.basename(csv)}')

        df = pd.read_csv(csv, skip_blank_lines=False, header=None)

        if clean_start:
            try:
                start = find_loc(df, clean_start)
                df = pd.read_csv(csv, skiprows=start)
            except (IndexError, KeyError):
                print(f'Start {cleaning_failure_message}')
                exit()

        if clean_end:
            try:
                end = find_loc(df, clean_end)
                df = df.loc[:end - 1]
            except (IndexError, KeyError):
                print(f'End {cleaning_failure_message}')
                exit()

        if filter_column:
            try:
                for value in filter_values:
                    df = df[~df[filter_column].str.contains(value)]
            except (IndexError, KeyError):
                print(f'Filter {cleaning_failure_message}')
                exit()

        df = df.dropna(axis=1, how='all')
        df.to_csv(csv, index=False)

def move_files(file, grab_from_folder, move_to_folder):
    """
    Moves file(s) to a new location.

    Parameters:
        file (str): File to be moved. Include full path.
        grab_from_folder (str): Folder path where file to be moved is located.
        move_to_folder (str): Folder path to move file to.
    """
    file_name = os.path.basename(file)
    print(f'Moving {file_name} to specified folder...')
    shutil.move(os.path.join(grab_from_folder, file_name), os.path.join(move_to_folder, file_name))