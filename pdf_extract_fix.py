from pdf_extract_utils import load_config, get_mmr_files, extract_and_export_tables

def main():
    config = load_config()
    pdf_pages_fix = input('Type the page numbers you need to adjust, separated by a comma: ')
    list_of_files = get_mmr_files(config)

    for file in list_of_files:
        extract_and_export_tables(file, config, pdf_pages_fix)

    print('Done.')

if __name__ == "__main__":
    main()