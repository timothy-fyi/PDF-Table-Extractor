from pdf_extract_utils import load_config, get_mmr_files, extract_and_export_tables

def main():
    config = load_config()

    list_of_files = get_mmr_files(config)

    for file in list_of_files:
        extract_and_export_tables(file, config, config['pdf_pages_to_extract'])

    print('Done.')

if __name__ == "__main__":
    main()