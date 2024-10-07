# PDF Table Extractor

# Set Up
1. Requires the PDF interpreter [Ghostscript](https://www.ghostscript.com/). Download and install.
2. Run ```pip install -r /path/to/requirements.txt``` to install required packages
3. Run ```pdf_data_extract.py```
4. The script will generate a ```config.yaml``` file and stop running
5. Edit the ```confg.yaml``` file, following the comments within it to ensure the correct values are being enetered
6. Re-run ```pdf_data_extract.py``` when ready to extract

# Additional Info
- The pages to extract from the PDF are declared in the config file, but there may be teams when this needs to change. One possibility is the PDF may be missing a page it normally contains, thowing off the page numbers where the tables usually are. If this happens, it is easy to adjust without updating the config file by using the ```pdf_extract_fix.py``` script. When running this script, instead of using the value from the configuration, it will ask you to input the page numbers instead. Ensure you are entering the page numbers on a single line, separated with commas like so: ```5,7,9,15```
- If the config file ever gets accidentally permanently deleted or corrupted, a new one can be generated by re-running ```pdf_data_extract.py```. Just ensure the config.yaml file is not in the script folder.
   
