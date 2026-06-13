from datetime import date

import csv
import re

from pathlib import Path

from src.patentapp_dataclass import PatentApp
from src.validation import validate_application

def data_extractrion_from_csv(input_file: Path) -> list:
    with open(input_file, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)
    rows = [{k.strip(): v for k, v in row.items()} for row in rows]
    return rows

def application_extraction(raw_data: list) -> list:
    applications: list[PatentApp] = []
    for row in raw_data:
        ipc_classes = _get_ipc_classes(row['IPC main class'], row['IPC secondary class(es)'])
        app_number = row['File number']
        title = row['Title']
        applicant = row['Applicant/owner']
        filing_date = _extract_date(row['Application date'])
        registration_date = _extract_date(row['Registration date']) if row['Registration date'] else None
        status: str = _get_status(row['Status'].lower(), registration_date) if row['Status'] else 'pending'
        data_dict = {
            'app_number': app_number,
            'title': title,
            'applicant': applicant,
            'filing_date': filing_date,
            'registration_date': registration_date,
            'status': status,
            'ipc_classes': ipc_classes
            }
        app = validate_application(data_dict)
        applications.append(app)
    print(applications)
    return applications

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
    if 'not pending' in status:
        return 'dead'
    elif 'pending' in status:
        if registration_date:
            return 'granted'
        else:
            return 'pending'
    else:
        return status
    
def _extract_date(date_str:str) -> date:
    try:
        return date.strptime(date_str, '%b %d, %Y')
    except ValueError:
        raise ValueError(f'{date_str} has wrong format. Provide date as e.g. 1 Jan, 2020.')