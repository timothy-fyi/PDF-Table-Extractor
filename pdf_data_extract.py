import os
from pdf_extract_utils import load_yaml, get_files, extract_and_export_tables, clean_csv, move_files, find_loc

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config_tn.yaml')
CONFIG_TEMPLATE = os.path.join(os.path.dirname(__file__), 'config_template.yaml')

def main():
    config = load_yaml(CONFIG_PATH, CONFIG_TEMPLATE)

    list_of_files = get_files(config['pdf_files'])
    if not list_of_files:
        print('There are no PDF files in the Unprocessed folder.')
        exit()

    for file in list_of_files:
        results = extract_and_export_tables(file=file, pages=config['pdf_pages_to_extract'], 
                                            export_folders=config['folder_names'], extract_date=True, flavor=config['flavor'])
        
        if config['optional_cleaning'] == 1:
            clean_csv(results, clean_start=config['clean_start'], clean_end=config['clean_end'], 
                      filter_column=config['filter_column'], filter_values=config['filter_values'])
            
        move_files(file, config['unprocessed_folder'], config['processed_folder'])

    print('Done.')

if __name__ == "__main__":
    main()