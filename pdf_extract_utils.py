import glob
import os
import shutil
import yaml
import camelot

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

def load_config():
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
        tables = camelot.read_pdf(file, flavor='stream', pages=pages)
    except IndexError:
        print('Pages not found. Did you input the correct page numbers?')
        exit()

    base_export_path = config['export_folder']
    folders = config['folder_names']

    for i, folder in enumerate(folders):
        file_path = os.path.join(base_export_path, folder, f'{folder.lower().replace(" ", "_")}{date_extract}.csv')
        tables[i].to_csv(file_path)

    print(f'Moving {file_name} to processed folder...')
    shutil.move(os.path.join(config['unprocessed_folder'], file_name), os.path.join(config['processed_folder'], file_name))
