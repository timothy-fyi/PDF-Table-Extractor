import glob
import os
import shutil
import yaml
import camelot
import pandas as pd

config_path = os.path.join(os.path.dirname(__file__), 'config_testing.yaml')
config_template = os.path.join(os.path.dirname(__file__), 'config_template.yaml')

def load_config():
    if not os.path.exists(config_path):
        shutil.copy(config_template, config_path)
        print('Config file missing. A new one has been created. You must open the new config.yaml file and define the variables.')
        exit()

    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)
    
def get_pdf_files(config):
    print('Getting PDF file(s)...')
    return glob.glob(config['pdf_files'])

def extract_and_export_tables(file, config, pages):
    file_name = os.path.basename(file)
    print(f'Extracting and exporting tables from {file_name} to csv...')
    date_extract = file[-8:-4]

    try:
        tables = camelot.read_pdf(file, flavor=config['flavor'], pages=pages, suppress_stdout=True)
    except IndexError:
        print('Pages not found. Did you input the correct page numbers?')
        exit()

    base_export_path = config['export_folder']
    folders = config['folder_names']

    for i, folder in enumerate(folders):
        file_path = os.path.join(base_export_path, folder, f'{folder.lower().replace(" ", "_")}{date_extract}.csv')

        try:
            tables[i].to_csv(file_path)
        except IndexError:
            print(
                f'ERROR: EXTRACT NOT SUCCESSFUL!\n'
                f'REASON: Pages in {file_name} seem to be image based.\n' 
                f'SOLUTION: Please check {file_name} and any other PDFs in the "Unprocessed" folder '
                f'and ensure that they are in the correct format, i.e. text based and NOT screenshot/image based.'
            )
            exit()

def clean_csv(file, config, clean_start=0, clean_end=0, filter=0):
    file_name = os.path.basename(file)
    date_extract = file[-8:-4]
    base_export_path = config['export_folder']
    folders = config['folder_names']
    cleaning_failure_message = (
        'column name in configuration not found. Did you set a name and did you spell it right? Did you mean to run the cleaning function?'
        'Note that while the CSVs exported, due to this failure they were NOT cleaned.'
        'Please check the configuration file and run the script again to clean CSVs.'
    )

    for folder in folders:
        file_path = os.path.join(base_export_path, folder, f'{folder.lower().replace(" ", "_")}{date_extract}.csv')

        print(f'Cleaning {os.path.basename(file_path)}')

        df = pd.read_csv(file_path, skip_blank_lines=False, header=None)

        if clean_start == 1:
            start_row = config['start_row_column_name']
            try:
                start = df.loc[df[0] == start_row].index[0]
                df = pd.read_csv(file_path, skiprows=start)
            except (IndexError, KeyError):
                print(f'Start {cleaning_failure_message}')
                exit()

        if clean_end == 1:
            end_row = config['end_row_column_name']
            ending_row_value = config['ending_row_value']
            try:
                df = df.loc[:df[df[end_row] == ending_row_value].index[0] - 1]
            except (IndexError, KeyError):
                print(f'End {cleaning_failure_message}')
                exit()

        if filter == 1:
            filter_column = config['filter_column']
            filter_values = config['filter_values']
            try:
                for value in filter_values:
                    df = df[~df[filter_column].str.contains(value)]
            except (IndexError, KeyError):
                print(f'Filter {cleaning_failure_message}')
                exit()

        df = df.dropna(axis=1, how='all')
        df.to_csv(file_path, index=False)

def move_pdf_files(file, config):
    file_name = os.path.basename(file)
    print(f'Moving {file_name} to processed folder...')
    shutil.move(os.path.join(config['unprocessed_folder'], file_name), os.path.join(config['processed_folder'], file_name))