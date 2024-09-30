import glob
import os
import shutil
import yaml
import camelot

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
config_template = os.path.join(os.path.dirname(__file__), 'config_template.yaml')

def load_config():
    if not os.path.exists(config_path):
        shutil.copy(config_template, config_path)
        print('Config file missing. A new one has been created. You must open the new config.yaml file and define the variables.')
        exit()

    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)
    
def get_mmr_files(config):
    print('Getting MMR file(s)...')
    return glob.glob(config['pdf_files'])

def extract_and_export_tables(file, config, pages):
    file_name = os.path.basename(file)
    print(f'Extracting and exporting tables from {file_name} to csv...')
    date_extract = file[-8:-4]

    try:
        tables = camelot.read_pdf(file, flavor='stream', pages=pages, suppress_stdout=True)
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

    print(f'Moving {file_name} to processed folder...')
    shutil.move(os.path.join(config['unprocessed_folder'], file_name), os.path.join(config['processed_folder'], file_name))
