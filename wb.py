"""Bulk Diglib Ingest Formatter

This script prepares files for use for Islandora Workbench as part of
the bulk ingest process for the APS Digital Library. It will properly
format all book objects for ingest and prepare the YAML file needed
for the ingest process.

The script requires a comma separated value file (.csv) prepared in
accordance with the APS template.

The script will return a YAML file and a CSV, both named with today's
date.

"""

import csv
import os
from ruamel.yaml import YAML
from datetime import datetime
import click


# set variables for local instance
username = 'username'
password = 'password'
host_path = 'http://localhost:8888'
workbench_path = '/your/path/to/workbench'
csv_path = '/path/to/data/folder'

def load_csv(path):
    """Returns CSV data as list of dictionaries"""
    rows = []
    with open(path, 'r') as f:
        csv_reader = csv.DictReader(f)
        fieldnames = csv_reader.fieldnames
        for row in csv_reader:
            rows.append(row)
    
    return fieldnames, rows


def validate_file_number(path, image_no):
    """Determines whether there are enough scans"""
    files = [f for f in os.listdir(path) if f.endswith('.tif')]
    if len(files) != int(image_no):
        raise ValueError(f'The number of files in {path} does not match the expected value')


def construct_path_names(base_path, path, image_no):
    """Constructs path names from a base path"""
    paths = []
    zfill = 3
    if len(image_no) > 3:
        zfill = len(image_no)
    for n in range(0, int(image_no)):
        file_name = f'{path}-{str(n + 1).zfill(zfill)}.tif'
        goal_path = os.path.join(base_path, path, file_name)
        paths.append(goal_path)
    
    return paths
    

def validate_file_names(base_path, path, image_no):
    """Determines whether file names match expected output"""
    paths = construct_path_names(base_path, path, image_no)
    path_to_check = os.path.join(base_path, path)
    files = [os.path.abspath(os.path.join(path_to_check, f)) for f in os.listdir(path_to_check) if f.endswith('.tif')]
    if set(paths) != set(files):
        raise ValueError(f'The file names in {path} do not match the expected values.')


def generate_rows(base_path, data, length):
    """Generate rows to append to CSV"""
    rows = []
    paths = construct_path_names(base_path, data['file'], data['total_scans'])
    count = length + 1
    headers = data.keys()
    for n, p in enumerate(paths, start=1):
        title = f'{data["title"]}, Page {str(n)}'
        params = {
            'file': p,
            'field_resource_type': 'Text',
            'field_model': 'Page',
            'title': title,
            'field_metadata_title': title,
            'id': str(count),
            'parent_id': data['id'],
            'field_weight': str(n),
            'field_display_hints': 'Open Seadragon'
        }
        row = {}
        for h in headers:
            if h in params.keys():
                row.update({h: params[h]})
            else:
                row.update({h: ''})
        rows.append(row)
        count = count + 1
    
    return rows


def generate_yaml():
    today = datetime.today().strftime('%Y-%m-%d')
    data = {
        'task': 'create',
        'host': host_path,
        'username': username,
        'password': password,
        'input_dir': csv_path,
        'input_csv': f'{today}.csv',
        'output_csv': f'{today}_output.csv',
        'output_csv_include_input_csv': True,
        'allow_missing_files': True,
        'allow_adding_terms': True,
        'validate_title_length': False,
        'perform_soft_checks': True,
        'standalone_media_url': True,
        'delete_tmp_upload': True,
        'adaptive_pause': 2,
        'adaptive_pause_threshold': 2.5,
        'log_term_creation': False,
        'http_cache_storage': 'memory',
        'http_cache_storage_expire_after': 600
    }
    yaml = YAML()
    with open(f'{workbench_path}/{today}.yml', 'w') as f:
        yaml.dump(data, f)

# put it all together in command line script

@click.command()
@click.argument('filename', type=click.Path(exists=True))
def cli(filename):
    """Generate a CSV and YAML file for diglib ingest.

    FILENAME should be the relative path to the CSV to process."""
    base_path = csv_path
    data_path = os.path.join(base_path, 'for_ingest')
    path = os.path.join(base_path, filename)
    fieldnames, data = load_csv(path)
    fieldnames.remove('total_scans')
    click.echo('File loaded, validating and generating data...')
    processed_data = []
    for row in data:
        row = dict(row)
        if row['total_scans'] != '':
            scan_no = row['total_scans']
            validate_file_number(os.path.join(data_path, row['file']), scan_no)
            validate_file_names(data_path, row['file'], scan_no)
            new_rows = generate_rows(data_path, row, len(data))
            data.extend(new_rows)
            row['file'] = ''
        row.pop('total_scans')
        processed_data.append(row)
    
    today = datetime.today().strftime('%Y-%m-%d')
    csv_output = f'{today}.csv'
    click.echo('Writing CSV file...')
    with open(os.path.join(base_path, csv_output), 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)
    click.echo('Writing YAML file...')
    generate_yaml()
    click.echo('Process completed.')


if __name__ == '__main__':
    cli()