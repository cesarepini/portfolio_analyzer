from dataclasses import asdict
import json

import dotenv

from datetime import date

import csv
import re

from pathlib import Path

from src.patentapp_dataclass import PatentApp
from src.validation import validate_application

def portfolio_extraction_from_csv():
    config = dotenv.dotenv_values('.env')
    input_file_name = input('Name of the file containing the portfolio:>')
    applications: list[PatentApp] = []
    if not input_file_name.endswith('.csv'):
        raise ValueError('The patent portfolio must be a .csv file.')
    try:
        file_path = Path(config['DATA_LOCATION_FOLDER']) / input_file_name
        with open(file_path, encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            for line in reader:
                # Extract and sanitize the inputs
                ipc_classes = _get_ipc_classes(line['IPC main class'], line['IPC secondary class(es)'])
                app_number = line['File number ']
                title = line['Title']
                applicant = line['Applicant/owner']
                filing_date = date.isoformat(date.strptime(line['Application date'], '%b %d, %Y')).replace('-', '')
                registration_date = line['Registration date']
                status: str = _get_status(line['Status'], registration_date)
                # Build the data dict
                data_dict = {
                        'app_number': app_number,
                        'title': title,
                        'applicant': applicant,
                        'filing_date': filing_date,
                        'status': status,
                        'ipc_classes': ipc_classes
                }
                # Verify the data_dict and create a PatentApp object
                app = validate_application(data_dict)
                # Append the PatentApp object to the the applications list
                applications.append(app)
    except FileNotFoundError:
        raise FileNotFoundError(f'File {input_file_name} not found.')
    
    try:
        output_file_name = input('Provide a name for the json file to save the portfolio data:>')
        output_file_name = output_file_name + '.json'
        file_path = Path(config['DATA_LOCATION_FOLDER']) / output_file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(app) for app in applications], f, default=str, indent=2, ensure_ascii=False)
    except Exception as e:
        raise e

def _get_ipc_classes(main_class: str, secondary_class: str):
    '''
    Function for extracting the ipc classes from the portfolio.
    '''
    ipc_classes = []
    main_class = re.sub(
        r'\([^(]*\)',
        '',
        main_class
    ).strip()
    ipc_classes.append(main_class)
    secondary_class = re.sub(
        r'\([^(]*\)',
        '',
        secondary_class
    ).strip()
    for sec_class in secondary_class.split(';'):
        if sec_class.strip() != '':
                ipc_classes.append(sec_class.strip())

    return ipc_classes

def _get_status(status: str, registration_date: str) -> str:
    if 'pending' in status:
        if registration_date:
            return 'granted'
        else:
             return 'pending'
    else:
        return 'dead'