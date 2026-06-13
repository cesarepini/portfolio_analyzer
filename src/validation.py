from datetime import date
from src.patentapp_dataclass import PatentApp

class ApplicationDataError(Exception):
    pass

def validate_application(data_dict: dict) -> PatentApp:
    exceptions = []
    # Checking if required field is missing
    if 'app_number' not in data_dict:
        exceptions.append('Missing application number.')
    if 'title' not in data_dict:
        exceptions.append('Missing title number.')
    if 'applicant' not in data_dict:
        exceptions.append('Missing applicant.')
    if 'filing_date' not in data_dict:
        exceptions.append('Missing filing date.')
    if exceptions:
        raise ApplicationDataError(' '.join(e for e in exceptions))

    # Validate the date: Check format and past date.
    if data_dict['filing_date'] > date.today():
        raise ValueError(f'Filing date {data_dict['filing_date']} is in the future. Please insert a filing date being less or equal than today.')
    
    # Validate the registration date (if present)
    if data_dict['registration_date']:
        if data_dict['registration_date'] < data_dict['filing_date'] or data_dict['registration_date'] > date.today():
            raise ValueError(f'Invalid registration date {data_dict['registration_date']}. Registration date must be between filig date and today (extremes included).')
    else:
        registration_date = None

    # Validate the status. Can be only pending, granted, dead (keep it simple for now)
    if data_dict['status'] not in ['pending', 'granted', 'dead']:
        raise ValueError(f'Invalid status {data_dict["status"]}')
    
    # If no error is raised, then return the data_dict formatted as PatentApplication
    return PatentApp(
        app_number = data_dict['app_number'],
        title = data_dict['title'],
        applicant = data_dict['applicant'],
        filing_date = data_dict['filing_date'],
        registration_date = data_dict['registration_date'],
        status = data_dict['status'],
        ipc_classes = data_dict.get('ipc_classes', [])
    )