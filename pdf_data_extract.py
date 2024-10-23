from testing_utils import load_config, get_pdf_files, extract_and_export_tables, clean_csv, move_pdf_files

def main():
    config = load_config()

    list_of_files = get_pdf_files(config)
    if not list_of_files:
        print('There are no PDF files in the Unprocessed folder.')
        exit()

    for file in list_of_files:
        extract_and_export_tables(file, config, config['pdf_pages_to_extract'])
        if config['optional_cleaning'] == 1:
            clean_csv(file, config, clean_start=config['clean_start'], clean_end=config['clean_end'], filter=config['filter'])
        move_pdf_files(file, config)

    print('Done.')

if __name__ == "__main__":
    main()