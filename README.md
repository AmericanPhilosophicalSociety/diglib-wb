# APS Workbench Preparation Script

This repository contains a script to prepare data for upload to one of the APS Islandora sites via [Islandora Workbench](https://github.com/mjordan/islandora_workbench). The script will produce a CSV with a row for each page in a book object.

# Configuring the script

Set the following variables according to your local installation and user profile:

- username
- password
- host_path
- workbench_path
- csv_path

Please contact an administrator or manager if you do not know the correct values.

# Preparing the data

Follow the instructions provided in the [APS Digital Library Metadata Guidelines](https://americanphilosophicalsociety.github.io/APS_digitization/metadata/), paying particular attention to the requirements for the field ['file'](https://americanphilosophicalsociety.github.io/APS_digitization/metadata/#file) and ['total scans'](https://americanphilosophicalsociety.github.io/APS_digitization/metadata/#total-scans).

Then, upload your image files and your data to the server with WinSCP. In the directory provided for "csv_path," there should be a folder labeled "for_ingest." In the "for_ingest" folder, create a folder for each manuscript, and give it the same name as the data provided in the 'file' field. Upload your image files to these folders. Then, upload the csv to the directory provided for "csv_path."

# Running the script

The script should also be uploaded to the server at the path specified for "csv_path." Run the script through the following command:

python3 wb.py {your-csv}.csv

where {your-csv}.csv is a name of a comma-separated values file in the same directory containing Paged Content you would like to ingest into the Digital Library. See the CDS Google Drive for a template for preparing this CSV.

## Sample data

The CSV "workbench_template.csv" and the images provided in "for_ingest/SMs_Coll_160_001" can be used as sample data to verify that the script runs.

# Outputs

The script will output two files:

- a CSV to run the Workbench process, at the file path specified for "csv_path". The CSV will be named after today's date.
- a YAML file to run the Workbench task, at the file path specified for "workbench_path". The YAML file will be named after today's date.

# Other uses

wb.py can also be imported as a module and run in another program.